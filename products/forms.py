from django import forms
from products.models import Product, Category
from django.core.validators import FileExtensionValidator
from io import StringIO
import csv
import re


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name',)


class ImportCSVForm(forms.Form):
    file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['csv'])]
    )

    def clean_file(self):
        csv_file = self.cleaned_data['file']
        reader = csv.DictReader(StringIO(csv_file.read().decode('utf-8')))
        for product in reader:
            product_object, _ = Product.objects.update_or_create(
                    name=product.get('name'),
                    defaults={
                        'description': product.get('description'),
                        'price': product.get('price'),
                        'sku': product.get('sku'),
                        'image': product.get('image')
                    }
                )
            for category_name in product.get('category').split(', '):
                category, _ = Category.objects.get_or_create(
                    name=re.sub(r"[^\w\s]", "", category_name)
                )
                product_object.category.add(category)
