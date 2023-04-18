from django.urls import path
from products.views import ProductsView, CategoriesView

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    path('categories/', CategoriesView.as_view(), name='categories')
]
