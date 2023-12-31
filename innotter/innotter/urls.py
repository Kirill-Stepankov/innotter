from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("page/", include("page.urls")),
    path("", include("post.urls")),
    path("tag/", include("tag.urls")),
]
