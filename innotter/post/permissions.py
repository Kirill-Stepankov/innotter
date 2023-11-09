from rest_framework.permissions import BasePermission

from .models import Post


class IsAdminOrIsOwnerOrIsModeratorOfTheOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user_data
            and request.user_data.get("role") == "Admin"
            or str(obj.page.owner) == request.user_data.get("uuid")
            or request.user_data.get("role") == "Moderator"
            and obj.page.owner_group_id == request.user_data.get("group_id")
        )
