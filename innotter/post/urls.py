from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import Feed, PostViewsSet

router = SimpleRouter()
router.register(r"post", PostViewsSet)


urlpatterns = router.urls

urlpatterns += [path("feed/", Feed.as_view())]
