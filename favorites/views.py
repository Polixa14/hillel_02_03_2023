from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from favorites.models import FavoriteProduct


class FavoriteView(ListView):
    model = FavoriteProduct
    template_name = 'favorite/index.html'
    context_object_name = 'favorite_products'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self, request, *args, **kwargs)

    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)

