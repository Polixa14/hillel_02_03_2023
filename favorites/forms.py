from django import forms
from favorites.models import FavoriteProduct
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from products.models import Product

User = get_user_model()


class AddProductToFavoriteForm(forms.Form):
    product = forms.UUIDField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self):
        try:
            product = Product.objects.get(id=self.cleaned_data.get('product'))
        except Product.DoesNotExist:
            raise ValidationError('Invalid product ID')
        favorite_product, created = FavoriteProduct.objects.get_or_create(
            user=self.user,
            product=product
        )
        if not created:
            favorite_product.delete()
