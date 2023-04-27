from django.views.generic import RedirectView
from django.urls import reverse_lazy
from orders.models import Order


class PaymentView(RedirectView):
    url = reverse_lazy('main')

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(
            is_active=True,
            is_paid=False,
            user=self.request.user
        )
        order.is_paid = True
        order.is_active = False
        order.save()
        return self.get(request, *args, **kwargs)
