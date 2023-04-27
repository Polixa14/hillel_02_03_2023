from django.urls import path
from orders.views import CartView, AddProductToCartView, OrderItemDeleteView, \
    UpdateQuantityCartView
urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('update/', UpdateQuantityCartView.as_view(), name='update_quantity'),
    path(
        'addproductocart/',
        AddProductToCartView.as_view(),
        name='add_to_cart'
    ),
    path(
        'deleteorderitem/<uuid:pk>',
        OrderItemDeleteView.as_view(),
        name='delete_item'
    )

]
