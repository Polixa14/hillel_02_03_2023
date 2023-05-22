import csv
import os
from django.core.files import File
from django.urls import reverse
from products.models import Product, Category
from project.settings import BASE_DIR


def test_products_list(client, product_factory):
    Product.objects.all().delete()
    for _ in range(10):
        product_factory()
    response = client.get(reverse('products'))
    assert response.status_code == 200
    assert len(response.context['products']) == Product.objects.count()


def test_product_by_category(client, product_factory, faker):
    for _ in range(10):
        product_factory()
    response = client.get(reverse('category_products',
                                  kwargs={'slug': faker.word()}))
    assert response.status_code == 404

    any_category = Category.objects.first()
    response = client.get(reverse('category_products',
                                  kwargs={'slug': any_category.slug}))
    assert response.status_code == 200
    assert response.context['products'].count() == \
           Product.objects.filter(category=any_category).count()


def test_export_csv(client, login_client):
    url = reverse('export-csv')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == \
           reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302
    client, user = login_client()
    response = client.get(url)
    products_data = response.content
    assert response.status_code == 200
    with open(os.path.join(BASE_DIR, 'test_files', 'products.csv'),
              'wb') as testfile:
        testfile.write(products_data)
    with open(os.path.join(BASE_DIR, 'test_files', 'products.csv'),
              'r') as file:
        csv_reader = csv.reader(file)
        row_count = sum(1 for row in csv_reader) - 1
    assert row_count == Product.objects.all().count()


def test_import_csv(client, login_client):
    url = reverse('import-csv')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == \
           reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302
    logged_client, user = login_client()
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == \
           reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302
    user.is_staff = True
    user.save()
    response = client.get(url)
    assert response.status_code == 200
    Product.objects.all().delete()
    with open(os.path.join(BASE_DIR, 'test_files', 'products1.csv'),
              'rt') as file:
        file_obj = File(file)
        response = logged_client.post(url, data={'file': file_obj})
    assert Product.objects.exists()
    assert response.status_code == 302

