import csv
from celery import shared_task
from project.celery import app
from products.models import Product, Category
from io import StringIO, BytesIO
import re
from products.clients.megasport_men import megasport_client
from django.core.files.images import ImageFile
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


@app.task
def import_csv_task(file_content):
    reader = csv.DictReader(StringIO(file_content))
    for product in reader:
        product_object, _ = Product.objects.update_or_create(
            name=product.get('name'),
            defaults={
                'description': product.get('description'),
                'price': product.get('price'),
                'sku': product.get('sku'),
                'image': product.get('image')
            }
        )
        for category_name in product.get('category').split(', '):
            category, _ = Category.objects.get_or_create(
                name=re.sub(r"[^\w\s]", "", category_name)
            )
            product_object.category.add(category)


@shared_task
def parce_megasport_task():
    products_list = megasport_client.prepared_data()
    if products_list:
        save_products_task.delay(products_list)


@app.task
def save_products_task(products_list):
    validate_url = URLValidator()
    for product in products_list:
        image_url = product.pop('image_url')
        category = product.pop('category')
        sku = product.pop('sku')
        product, _ = Product.objects.update_or_create(
            sku=sku,
            defaults=product
        )
        try:
            validate_url(image_url)
        except ValidationError:
            pass
        else:
            image_data = megasport_client.get_image(image_url)
            image = ImageFile(BytesIO(image_data.content), name=image_url)
            product.image = image
            product.save(update_fields=('image',))

        product_category, _ = Category.objects.get_or_create(name=category)
        product.category.add(product_category)
