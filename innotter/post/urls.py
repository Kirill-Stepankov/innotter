from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import Feed, PostViewsSet

router = SimpleRouter()
router.register(r"post", PostViewsSet)


urlpatterns = [path("", include(router.urls)), path("feed/", Feed.as_view())]
