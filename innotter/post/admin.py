from django.contrib import admin

from .models import Likes, Post

admin.site.register(Post)
admin.site.register(Likes)
