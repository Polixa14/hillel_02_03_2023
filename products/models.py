import uuid
from os import path
from django.db import models
from multiselectfield import MultiSelectField


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to=upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class Discount(models.Model):

    CASH_DISCOUNT = 0
    PERCENT_DISCOUNT = 1
    DISCOUNT_CHOICES = (
        (CASH_DISCOUNT, 'Cash discount'),
        (PERCENT_DISCOUNT, 'Percentage discount')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.PositiveIntegerField()
    code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    discount_type = models.IntegerField(choices=DISCOUNT_CHOICES)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to=upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.PositiveIntegerField()
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True)

