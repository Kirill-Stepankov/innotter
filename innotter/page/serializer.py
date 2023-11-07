from rest_framework.serializers import ModelSerializer

from .models import Page


class PageSerializer(ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"
        read_only_fields = (
            "owner",
            "owner_group_id",
            "image",
            "created_at",
            "updated_at",
            "is_blocked",
        )
        extra_kwargs = {"owner": {"required": False}}
