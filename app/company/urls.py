"""URL mappings for the company app."""

from rest_framework_nested import routers
from django.urls import path, include

from company.views import CompanyViewSet
from card.views import CardViewSet

router = routers.SimpleRouter()
router.register(r'', CompanyViewSet)

companies_router = routers.NestedSimpleRouter(router, r'', lookup='company')
companies_router.register(r'card', CardViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(companies_router.urls)),
]
