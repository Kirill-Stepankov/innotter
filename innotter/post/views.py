from page.models import Followers
from page.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Post
from .permissions import IsAdminOrIsOwnerOrIsModeratorOfTheOwnerOfPost
from .serializer import PostSerializer


class PostViewsSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Post.objects.all().prefetch_related("page")
    serializer_class = PostSerializer
    permission_classes_by_action = {
        "update": [IsAdminOrIsOwnerOrIsModeratorOfTheOwnerOfPost],
        "partial_update": [IsAdminOrIsOwnerOrIsModeratorOfTheOwnerOfPost],
        "destroy": [IsAdminOrIsOwnerOrIsModeratorOfTheOwnerOfPost],
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class Feed(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        followers = Followers.objects.filter(
            user=request.user_data.get("uuid")
        ).select_related("page")
        posts = Post.objects.filter(page__follows__in=followers)

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)
