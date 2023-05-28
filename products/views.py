import csv
from django.views.generic import DetailView, View, FormView, \
    ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from favorites.models import FavoriteProduct
from products.models import Category, Product
from products.forms import ImportCSVForm
from django.http import HttpResponse, Http404
from products.tasks import parce_megasport_task


class ProductsView(ListView):
    model = Product
    context_object_name = 'products'
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        parce_megasport_task.delay()
        return super().get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_favorites'] = \
                [product.product.sku for product
                 in FavoriteProduct.objects.filter(user=self.request.user)]
        return context


class CategoriesView(ListView):
    model = Category
    context_object_name = 'categories'


class CategoryProductsView(ListView):
    model = Product
    template_name = 'products/category_products.html'
    paginate_by = 20

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.category = Category.objects.get(slug=kwargs['slug'])
        except Category.DoesNotExist:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(category__in=(self.category,))

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
