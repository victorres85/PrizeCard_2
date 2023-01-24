"""URL mappings for the company app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shopper.views import ShopperViewset

router = DefaultRouter()
router.register('', ShopperViewset)


app_name = 'shopper'

urlpatterns = [
    path('', include(router.urls))
]
