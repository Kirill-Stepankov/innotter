from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import SimpleRouter

from .views import PageViewSet

router = SimpleRouter()
router.register(r"page", PageViewSet)


urlpatterns = router.urls
