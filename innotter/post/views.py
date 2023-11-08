from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Post
from .permissions import IsAdminOrIsOwnerOrIsModeratorOfTheOwner
from .serializer import PostSerializer


class PostViewsSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Post.objects.all().prefetch_related("page")
    serializer_class = PostSerializer
    permission_classes_by_action = {
        "update": [IsAdminOrIsOwnerOrIsModeratorOfTheOwner],
        "partial_update": [IsAdminOrIsOwnerOrIsModeratorOfTheOwner],
        "destroy": [IsAdminOrIsOwnerOrIsModeratorOfTheOwner],
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]
