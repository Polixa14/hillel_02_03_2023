from django.db import models
from django.contrib.auth import get_user_model
from project.mixins.models import PKMixin
from project.model_choices import Rating


class Feedback(PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        choices=Rating.choices,
        default=Rating.FIVE_STARS
    )

    class Meta:
        ordering = ['-created_at']
