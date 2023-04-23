from django.urls import reverse_lazy
from orders.models import Order, OrderItem
from django.views.generic import TemplateView, RedirectView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from products.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from payments.models import Discount


class CartView(TemplateView):
    template_name = 'orders/cart.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            order = Order.objects.get(
                user=self.request.user,
                is_paid=False
            )
            context.update(
                {
                    'order': order,
                    'order_items': OrderItem.objects.filter(order=order),
                    'discounts': Discount.objects.filter(is_active=True)
                }
            )
        except ObjectDoesNotExist:
            pass
        return context

    def post(self, request, *args, **kwargs):
        quantity = request.POST.get('quantity')
        order_item_id = request.POST.get('order_item_id')
        discount_code = request.POST.get('discount_code')
        order = self.get_context_data(**kwargs).get('order')
        try:
            order.discount = Discount.objects.get(code=discount_code)
            order.save()
        except ObjectDoesNotExist:
            pass
        if order_item_id:
            order_item = OrderItem.objects.get(id=order_item_id)
            order_item.quantity = quantity
            order_item.save()
            order_item.order.save()
        return redirect('cart', *args, **kwargs)


class AddProductToCartView(RedirectView):

    def get_redirect_url(self, slug, *args, **kwargs):
        order, created = Order.objects.get_or_create(
            user=self.request.user,
            is_paid=False,
        )
        product = Product.objects.get(slug=slug)
        if created:
            order.order_number = \
                Order.objects.filter(user=self.request.user).count()
            order.save()

        if not OrderItem.objects.filter(order=order, product=product).exists():
            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=1
            )
        return reverse_lazy('cart')


class OrderItemDeleteView(DeleteView):
    model = OrderItem
    success_url = reverse_lazy('cart')
