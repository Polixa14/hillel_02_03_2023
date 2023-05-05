# Generated by Django 4.1.7 on 2023-04-30 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.CharField(choices=[('UAH', 'UAH'), ('USD', 'USD'), ('EUR', 'EUR')], default='UAH', max_length=16),
        ),
    ]