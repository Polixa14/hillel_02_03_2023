from django.dispatch import receiver
from django.db.models.signals import pre_save
from orders.models import Order


@receiver(pre_save, sender=Order)
def pre_save_order_signal(sender, instance, **kwargs):
    instance.total_price = instance.calc_total_price
    instance.total_price_with_discount = instance.calc_price_with_discount

