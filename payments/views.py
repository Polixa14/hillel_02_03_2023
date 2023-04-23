from django.views.generic import RedirectView
from django.urls import reverse_lazy
from orders.models import Order


class PaymentView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        order = Order.objects.get(
            user=self.request.user,
            is_paid=False,
        )
        order.is_paid = True
        order.save()
        return reverse_lazy('main')
