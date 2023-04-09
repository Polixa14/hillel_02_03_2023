from django.db import models
from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin


class Stock(PKMixin):
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True
    )
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    quantity = models.PositiveSmallIntegerField()
