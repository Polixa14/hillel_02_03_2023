from django.contrib import admin

from products.models import Product, Category, Discount

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass
