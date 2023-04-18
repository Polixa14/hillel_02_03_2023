from django.urls import path
from favorites.views import FavoriteView, AddToFavoriteProduct

urlpatterns = [
    path('', FavoriteView.as_view(), name='favorite'),
    path(
        'addfavorite/<slug:slug>/',
        AddToFavoriteProduct.as_view(),
        name='add_to_favorite'
    )
]
