from django.contrib import messages
from django.urls import reverse_lazy
from orders.models import OrderItem
from django.views.generic import FormView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from orders.mixins import GetOrderMixin
from orders.forms import UpdateQuantityCartForm, CartForm, AddProductToCartForm
from django.utils.translation import gettext_lazy as _


class CartView(GetOrderMixin, FormView):
    template_name = 'orders/cart.html'
    success_url = reverse_lazy('cart')
    form_class = CartForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'order': self.get_order(),
        })
        return context

    def form_valid(self, form):
        form.instance = self.get_order()
        form.save()
        messages.success(self.request, _('Discount applied'))
        return super().form_valid(form)


class UpdateQuantityCartView(GetOrderMixin, FormView):
    template_name = 'orders/cart.html'
    form_class = UpdateQuantityCartForm
    success_url = reverse_lazy('cart')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddProductToCartView(GetOrderMixin, FormView):
    template_name = 'products/product_detail.html'
    form_class = AddProductToCartForm
    success_url = reverse_lazy('cart')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('Product added to cart'))
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'order': self.get_order()
        })
        return kwargs


class OrderItemDeleteView(DeleteView):
    model = OrderItem
    success_url = reverse_lazy('cart')
