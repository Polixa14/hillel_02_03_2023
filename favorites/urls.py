from django.urls import path
from favorites.views import FavoriteView

urlpatterns = [
    path('', FavoriteView.as_view(), name='favorite')
]
