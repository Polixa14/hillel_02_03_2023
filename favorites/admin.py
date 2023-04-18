from django.contrib import admin
from favorites.models import FavoriteProduct


@admin.register(FavoriteProduct)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('product', 'group_name')
