from orders.models import Order


class GetOrderMixin:
    def get_order(self):
        order, created = Order.objects.get_or_create(
            is_active=True,
            is_paid=False,
            user=self.request.user
        )
        if created:
            order_num = Order.objects.count()
            order.order_number = order_num
            order.save()
        return order
