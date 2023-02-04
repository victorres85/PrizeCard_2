"""URL mappings for the company app."""

from rest_framework_nested import routers
from django.urls import path, include

from shopper.views import ShopperViewset
from mycards.views import MycardsViewSet
from mycardshistory.views import MycardsHistoryViewSet

router = routers.SimpleRouter()
router.register(r'', ShopperViewset)

shoppers_router = routers.NestedSimpleRouter(router, r'', lookup='shopper')
shoppers_router.register(r'mycards', MycardsViewSet)
shoppers_router.register(r'mycardshistory', MycardsHistoryViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(shoppers_router.urls)),
]
