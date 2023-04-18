from os import path
from django.db import models
from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from django.utils.text import slugify


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to=upload_to)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to=upload_to)
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category)
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        counter = 1
        while Product.objects.filter(slug=self.slug).exists():
            self.slug = f'{slugify(self.name)}-{counter}'
            counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)
