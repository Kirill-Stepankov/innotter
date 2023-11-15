from django.db import models
from tag.models import Tag


class Page(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="pages")
    owner = models.UUIDField(null=True, blank=True)
    owner_group_id = models.IntegerField(null=True, blank=True)
    owner_email = models.EmailField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated_at"]


class Followers(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="follows")
    user = models.UUIDField()
