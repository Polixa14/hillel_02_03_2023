import csv
from project.celery import app
from products.models import Product, Category
from io import StringIO
import re


@app.task()
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
