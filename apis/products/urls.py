from rest_framework import routers
from apis.products.views import ProductViewSet


router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
urlpatterns = router.urls
