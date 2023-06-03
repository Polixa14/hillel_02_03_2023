from django.contrib import admin
from products.models import Product, Category
from django.utils.safestring import mark_safe


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'price',
                    'is_active',
                    'image_display',
                    'created_at')
    filter_horizontal = ('category',)

    @admin.display(description='Image')
    def image_display(self, obj):
        return mark_safe(
            '<img src="{}" width=64, height="64" />'.format(obj.image.url)
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_display')

    @admin.display(description='Image')
    def image_display(self, obj):
        return mark_safe(
            '<img src="{}" width=64, height="64" />'.format(obj.image.url)
        ) if obj.image else 'No image'
