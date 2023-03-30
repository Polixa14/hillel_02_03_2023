from decimal import Decimal
from django.db import models
from payments.models import Discount
from products.models import Product
from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from django.contrib.auth.models import User


class Order(PKMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    total_price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )

    @property
    def calc_total_price(self):
        total_price = 0
        for item in self.orderitem_set.all():
            total_price += item.price
        return total_price

    def __str__(self):
        return str(self.order_number)

    def save(self, *args, **kwargs):
        self.total_price = self.calc_total_price
        super(Order, self).save(*args, **kwargs)


class OrderItem(PKMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField()
    discounts = models.ManyToManyField(Discount, blank=True)
    price = models.DecimalField(
        null=True,
        blank=True,
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )

    @property
    def price_with_discount(self):
        price_with_discount = self.product.price * self.quantity
        for discount in self.discounts.all():
            if discount.discount_type == 1:
                price_with_discount = \
                    price_with_discount * (Decimal('1') -
                                           Decimal(str(discount.amount)) /
                                           Decimal('100'))
            elif discount.discount_type == 0:
                price_with_discount = price_with_discount - \
                                      Decimal(discount.amount)
        return price_with_discount

    def save(self, *args, **kwargs):
        self.price = self.price_with_discount
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} {self.quantity}'
