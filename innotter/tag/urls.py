from rest_framework.routers import SimpleRouter

from .views import TagViewSet

router = SimpleRouter()
router.register(r"", TagViewSet)


urlpatterns = router.urls
