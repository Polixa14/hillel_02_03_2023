from rest_framework import serializers
from products.models import Product


class ProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'currency', 'description', 'image',
                  'category', 'category_name')

    def get_category_name(self, obj):
        return obj.category.values_list('name', flat=True)
