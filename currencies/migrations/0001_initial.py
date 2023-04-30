# Generated by Django 4.1.7 on 2023-04-30 10:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticker', models.CharField(choices=[('UAH', 'UAH'), ('USD', 'USD'), ('EUR', 'EUR')], default='UAH', max_length=16)),
                ('buy', models.DecimalField(decimal_places=2, default=1, max_digits=12)),
                ('sell', models.DecimalField(decimal_places=2, default=1, max_digits=12)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
