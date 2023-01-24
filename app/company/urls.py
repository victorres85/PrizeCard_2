"""URL mappings for the company app."""

from rest_framework.routers import DefaultRouter

from company import views

router = DefaultRouter(trailing_slash=True)
router.register('', views.CompanyViewSet)

app_name = 'company'

urlpatterns = router.urls
