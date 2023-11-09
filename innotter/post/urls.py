from rest_framework.routers import SimpleRouter

from .views import PostViewsSet

router = SimpleRouter()
router.register(r"post", PostViewsSet)


urlpatterns = router.urls
