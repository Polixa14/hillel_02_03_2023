from django import forms
from orders.models import OrderItem
from payments.models import Discount
from django.core.exceptions import ValidationError
from products.models import Product


class UpdateQuantityCartForm(forms.Form):
    quantity = forms.IntegerField()

    def __init__(self, order_item_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_item = OrderItem.objects.get(id=order_item_id)
        self.fields['quantity'].initial = self.order_item.quantity

    def save(self):
        self.order_item.quantity = self.cleaned_data.get('quantity')
        self.order_item.save()


class CartForm(forms.Form):
    discount = forms.CharField(required=False)

    def clean_discount(self):
        try:
            discount = Discount.objects.get(
                code=self.cleaned_data.get('discount')
            )
        except Discount.DoesNotExist:
            raise ValidationError('Invalid discount code')
        if not discount.is_valid:
            raise ValidationError('Discount expired')
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
            raise ValidationError('Invalid product ID')
        return product

    def save(self):
        product = self.cleaned_data.get('product')
        order_item, _ = OrderItem.objects.get_or_create(
            order=self.order,
            product=product,
            price=product.price,
            quantity=1
        )
