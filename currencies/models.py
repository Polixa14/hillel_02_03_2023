from django.db import models
from project.model_choices import CurrencyChoices
from project.mixins.models import PKMixin
from project.constants import MAX_DIGITS, DECIMAL_PLACES


class CurrencyHistory(PKMixin):
    ticker = models.CharField(
        max_length=16,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.UAH
    )
    buy = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )
    sell = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.ticker} - {self.buy} / {self.sell}'
