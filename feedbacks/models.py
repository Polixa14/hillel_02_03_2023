from django.db import models
from django.contrib.auth import get_user_model
from project.mixins.models import PKMixin
from django.core.validators import MaxValueValidator
from django.core.cache import cache
from project.model_choices import FeedbacksCacheKeys
from django_lifecycle import LifecycleModelMixin, hook, AFTER_SAVE, \
    AFTER_DELETE


class Feedback(LifecycleModelMixin, PKMixin):
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

    @hook(AFTER_SAVE)
    @hook(AFTER_DELETE)
    def clean_cache_signal(self):
        cache.delete(FeedbacksCacheKeys.FEEDBACKS)
