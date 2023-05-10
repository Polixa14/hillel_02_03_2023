from django import forms
from orders.models import OrderItem
from payments.models import Discount
from django.core.exceptions import ValidationError
from products.models import Product
from django.utils.translation import gettext_lazy as _


class UpdateQuantityCartForm(forms.Form):
    quantity = forms.IntegerField()
    order_item = forms.UUIDField()

    def save(self):
        order_item = self.cleaned_data.get('order_item')
        order_item.quantity = self.cleaned_data.get('quantity')
        order_item.save()

    def clean_order_item(self):
        try:
            order_item = OrderItem.objects.get(
                id=self.cleaned_data.get('order_item')
            )
        except OrderItem.DoesNotExist:
            raise ValidationError(_('Invalid Order Item ID'))
        return order_item


class CartForm(forms.Form):
    discount = forms.CharField(required=False)

    def clean_discount(self):
        try:
            discount = Discount.objects.get(
                code=self.cleaned_data.get('discount')
            )
        except Discount.DoesNotExist:
            raise ValidationError(_('Invalid discount code'))
        if not discount.is_valid:
            raise ValidationError(_('Discount expired'))
        return discount

    def save(self):
        self.instance.discount = self.cleaned_data.get('discount')
        self.instance.save()


class AddProductToCartForm(forms.Form):
    product = forms.UUIDField()

    def __init__(self, order, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = order

    def clean_product(self):
        try:
            product = Product.objects.get(id=self.cleaned_data.get('product'))
        except Product.DoesNotExist:
            raise ValidationError(_('Invalid product ID'))
        return product

    def save(self):
        product = self.cleaned_data.get('product')
        order_item, _ = OrderItem.objects.get_or_create(
            order=self.order,
            product=product,
            price=product.price,
            quantity=1
        )
