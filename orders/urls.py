from django.urls import path
from orders.views import CartView, AddProductToCartView, OrderItemDeleteView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path(
        'addproductocart/<slug:slug>/',
        AddProductToCartView.as_view(),
        name='add_to_cart'
    ),
    path(
        'deleteorderitem/<uuid:pk>',
        OrderItemDeleteView.as_view(),
        name='delete_item'
    )
]
