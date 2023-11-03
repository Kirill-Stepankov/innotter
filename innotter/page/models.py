from django.db import models
from tag.models import Tag


class Page(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="pages")
    owner = models.UUIDField()
    image = models.URLField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Followers(models.Model):
    post = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="follows")
    user = models.UUIDField()
