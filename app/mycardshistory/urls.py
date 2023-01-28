"""URL mappings for the mycards app."""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from mycardshistory import views

router = DefaultRouter()
router.register(r'', views.MycardsViewSet)

app_name = 'mycardshistory'

urlpatterns = [
    path('', include(router.urls))
]
