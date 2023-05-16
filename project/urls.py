"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.urls import urlpatterns as accounts_urlpatterns
from feedbacks.urls import urlpatterns as feedbacks_urlpatterns
from products.urls import urlpatterns as products_urlpatterns
from main.urls import urlpatterns as main_urlpatterns
from favorites.urls import urlpatterns as favorite_urlpatterns
from orders.urls import urlpatterns as orders_urlpatterns
from payments.urls import urlpatterns as payments_urlpatterns
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

i18n_urlpatterns = [
    path('products/', include(products_urlpatterns)),
    path('feedbacks/', include(feedbacks_urlpatterns)),
    path('accounts/', include(accounts_urlpatterns)),
    path('favorite/', include(favorite_urlpatterns)),
    path('orders/', include(orders_urlpatterns)),
    path('payments/', include(payments_urlpatterns)),
    path('', include(main_urlpatterns)),
]

urlpatterns = [
    path('i18n/', include("django.conf.urls.i18n")),
    path('admin/', admin.site.urls),
]

urlpatterns = urlpatterns + i18n_patterns(*i18n_urlpatterns)

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]
