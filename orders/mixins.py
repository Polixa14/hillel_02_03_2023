from orders.models import Order


class GetOrderMixin:
    def get_order(self):
        order, created = Order.objects.get_or_create(
            is_active=True,
            is_paid=False,
            user=self.request.user
        )
        return order
