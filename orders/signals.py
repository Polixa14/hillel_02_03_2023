from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from orders.models import Order, OrderItem


@receiver(pre_save, sender=Order)
def pre_save_order_signal(sender, instance, **kwargs):
    if not instance.order_number:
        instance.order_number = Order.objects.count() + 1
    instance.total_price = instance.calc_total_price
    instance.total_price_with_discount = instance.calc_price_with_discount


@receiver(post_save, sender=OrderItem)
def post_save_order_item_signal(sender, instance, **kwargs):
    instance.order.save()


@receiver(post_delete, sender=OrderItem)
def post_delete_order_item_signal(sender, instance, **kwargs):
    instance.order.save()
