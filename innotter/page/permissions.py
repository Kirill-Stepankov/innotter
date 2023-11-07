from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user_data)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user_data and request.user_data.get("role") == "Admin")


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user_data and request.user_data.get("role") == "Moderator")


class IsPageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user_data and str(obj.owner) == request.user_data.get("uuid")
        )


class IsModeratorOfThePageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user_data
            and request.user_data.get("role") == "Moderator"
            and obj.owner_group_id == request.user_data.get("group_id")
        )


class IsAdminOrIsOwnerOrIsModeratorOfTheOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user_data
            and request.user_data.get("role") == "Admin"
            or str(obj.owner) == request.user_data.get("uuid")
            or request.user_data.get("role") == "Moderator"
            and obj.owner_group_id == request.user_data.get("group_id")
        )
