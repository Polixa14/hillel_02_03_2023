from django.urls import path
from favorites.views import FavoriteView, AJAXAddToFavoriteProduct

urlpatterns = [
    path('', FavoriteView.as_view(), name='favorite'),
    path(
        'add-favorite/<uuid:pk>',
        AJAXAddToFavoriteProduct.as_view(),
        name='add_to_favorite'
    )
]
