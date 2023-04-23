from django.dispatch import receiver
from django.db.models.signals import post_save
from orders.models import Order


# @receiver(post_save, sender=Order)
# def post_save_order_signal(sender, instance, **kwargs):
#     # total_price = instance.calc_total_price
#     # Order.objects.filter(id=instance.id).update(total_price=total_price)
#     total_price_with_discount = instance.calc_price_with_discount
#     Order.objects.filter(id=instance.id).update(
#         total_price_with_discount=total_price_with_discount
#     )

