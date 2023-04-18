from django.db import models
from django.contrib.auth import get_user_model
from project.mixins.models import PKMixin


class FavoriteProduct(PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    group_name = models.CharField(
        max_length=255,
        default='Your favorite products'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('product', 'group_name', 'user')
