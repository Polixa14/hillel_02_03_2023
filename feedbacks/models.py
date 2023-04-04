from django.db import models
from django.contrib.auth import get_user_model
from project.mixins.models import PKMixin
from django.core.validators import MaxValueValidator


class Feedback(PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(5),)
    )

    class Meta:
        ordering = ('-created_at',)
