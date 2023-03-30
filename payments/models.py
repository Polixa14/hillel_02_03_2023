from django.db import models
from project.mixins.models import PKMixin


class Discount(PKMixin):

    CASH_DISCOUNT = 0
    PERCENT_DISCOUNT = 1
    DISCOUNT_CHOICES = (
        (CASH_DISCOUNT, 'Cash discount'),
        (PERCENT_DISCOUNT, 'Percentage discount')
    )

    amount = models.PositiveIntegerField()
    code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    discount_type = models.IntegerField(choices=DISCOUNT_CHOICES)

    def __str__(self):
        return self.code
