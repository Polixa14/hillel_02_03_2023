from django.utils import timezone
from django.db import models
from project.constants import DECIMAL_PLACES, MAX_DIGITS
from project.mixins.models import PKMixin
from project.model_choices import DiscountTypes


class Discount(PKMixin):

    CASH_DISCOUNT = 0
    PERCENT_DISCOUNT = 1
    DISCOUNT_CHOICES = (
        (CASH_DISCOUNT, 'Cash discount'),
        (PERCENT_DISCOUNT, 'Percentage discount')
    )

    amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE
    )
    valid_until = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.code

    @property
    def is_valid(self):
        is_valid = self.is_active
        if self.valid_until:
            is_valid &= timezone.now() <= self.valid_until
        return is_valid
