from datetime import timedelta
import django_filters
from django.utils import timezone
from products.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    sku = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.RangeFilter()
    date = django_filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Product
        fields = ['price', 'name', 'sku', 'date']
