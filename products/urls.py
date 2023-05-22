from django.urls import path
from products.views import ProductsView, ProductDetailView, \
    ExportCsv, ImportCsv, CategoryProductsView

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path(
        'categories/<slug:slug>/',
        CategoryProductsView.as_view(),
        name='category_products'
    ),
    path(
        'details/<slug:slug>/',
        ProductDetailView.as_view(),
        name='details'
    ),
    path('exprot-csv/', ExportCsv.as_view(), name='export-csv'),
    path('import-csv/', ImportCsv.as_view(), name='import-csv')
]
