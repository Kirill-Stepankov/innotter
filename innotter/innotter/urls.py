from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("page.urls")),
    path("", include("post.urls")),
    path("", include("tag.urls")),
]
