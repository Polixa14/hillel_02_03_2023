from decimal import Decimal
from django.db import models
from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from django.contrib.auth import get_user_model
from project.model_choices import DiscountTypes


class Order(PKMixin):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    total_price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    total_price_with_discount = models.DecimalField(
        null=True,
        blank=True,
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    discount = models.ForeignKey(
        'payments.Discount',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    @property
    def calc_total_price(self):
        total_price = 0
        for item in self.order_items.iterator():
            total_price += item.price * item.quantity
        return total_price

    def __str__(self):
        return str(self.order_number)

    @property
    def calc_price_with_discount(self):
        price_with_discount = self.total_price
        if self.discount and self.discount.is_valid:
            if self.discount.discount_type == DiscountTypes.PERCENT:
                price_with_discount = \
                    self.total_price * \
                    (Decimal(1) - self.discount.amount / Decimal(100))
            else:
                if self.total_price < self.discount.amount:
                    pass
                else:
                    price_with_discount = \
                        self.total_price - self.discount.amount
        return price_with_discount


class OrderItem(PKMixin):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True
    )
    is_active = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )

    def save(self, *args, **kwargs):
        self.price = self.product.price_in_uah
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} {self.quantity}'

    class Meta:
        ordering = ('-created_at',)
