from django.contrib import admin
from stocks.models import Stock


@admin.register(Stock)
class PStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'price')
