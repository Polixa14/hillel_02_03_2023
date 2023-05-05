from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from feedbacks.models import Feedback
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Feedback)
def post_save_delete_feedback_signal(sender, instance, **kwargs):
    cache.delete('feedbacks')
