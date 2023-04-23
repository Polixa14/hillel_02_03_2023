import csv
from django.views.generic import TemplateView, DetailView, View, FormView, \
    ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from favorites.models import FavoriteProduct
from products.models import Category, Product
from products.forms import ImportCSVForm
from django.http import HttpResponse


class ProductsView(ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'
    paginate_by = 20


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_favorites'] = \
                [product.product.sku for product
                 in FavoriteProduct.objects.filter(user=self.request.user)]

        return context


class CategoriesView(TemplateView):
    template_name = 'products/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.iterator()
        return context


class CategoryProductsView(TemplateView):
    template_name = 'products/category_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['products'] = Product.objects.filter(
            category=context['category']
        )
        return context


class ExportCsv(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename="products.csv"'
            }
        )
        fields = ['name', 'description', 'price', 'category', 'sku', 'image']
        writer = csv.DictWriter(response, fieldnames=fields)
        writer.writeheader()
        for product in Product.objects.iterator():
            writer.writerow(
                {
                 'name': product.name,
                 'description': product.description,
                 'price': product.price,
                 'category': [
                     category.name for category in product.category.all()
                 ],
                 'sku': product.sku,
                 'image': product.image.name if product.image else 'no image'
                }
            )
        return response


class ImportCsv(FormView):
    form_class = ImportCSVForm
    template_name = 'products/import_csv.html'
    success_url = reverse_lazy('products')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
