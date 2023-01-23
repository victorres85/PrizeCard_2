"""URL mappings for the company app."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from company import views

router = DefaultRouter()
router.register('', views.CompanyViewSet)

app_name = 'company'

urlpatterns = [
    path('', include(router.urls))
]
