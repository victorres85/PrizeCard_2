"""URL mappings for the card app."""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from card import views

router = DefaultRouter()
router.register(r'', views.CardViewSet)

app_name = 'card'

urlpatterns = [
    path('', include(router.urls))
]
