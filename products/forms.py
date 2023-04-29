from django import forms
from products.models import Product
from django.core.validators import FileExtensionValidator
from products.tasks import import_csv_task


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
        file_content = csv_file.read().decode('utf-8')
        import_csv_task.delay(file_content)
