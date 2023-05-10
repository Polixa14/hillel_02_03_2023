from django.contrib import messages
from django.views.generic import RedirectView
from django.urls import reverse_lazy
from orders.models import Order
from django.utils.translation import gettext_lazy as _


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
        messages.success(self.request, _('Order paid'))
        return self.get(request, *args, **kwargs)
