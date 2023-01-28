"""URL mappings for the company app."""

from rest_framework_nested import routers
from django.urls import path, include

from shopper.views import ShopperViewset
from mycards.views import MycardsViewSet

router = routers.SimpleRouter()
router.register(r'', ShopperViewset)

shoppers_router = routers.NestedSimpleRouter(router, r'', lookup='shopper')
shoppers_router.register(r'mycards', MycardsViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(shoppers_router.urls)),
]
