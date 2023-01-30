"""URL mappings for the company app."""

from rest_framework_nested import routers
from django.urls import path, include

from company.views import CompanyViewSet, CompanyLogoViewSet
from card.views import CardViewSet

router = routers.SimpleRouter()
router.register(r'', CompanyViewSet)

companies_router = routers.NestedSimpleRouter(router, r'', lookup='company')
companies_router.register(r'card', CardViewSet)
companies_router.register(r'logo', CompanyLogoViewSet, basename='logo-company')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(companies_router.urls)),
]
