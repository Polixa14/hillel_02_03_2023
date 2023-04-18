from django.views.generic import TemplateView
from products.models import Category, Product


class ProductsView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.iterator()
        return context


class CategoriesView(TemplateView):
    template_name = 'products/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.iterator()
        return context
