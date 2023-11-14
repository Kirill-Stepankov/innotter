from page.models import Followers
from page.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from innotter.producer import kafka_producer

from .models import Likes, Post
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

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        like = self._like(request.user_data, pk)

        payload = {"page_id": pk, "type": "like"}
        kafka_producer.produce_message("posts", payload)

        return Response(data={"detail": "Post is liked."})

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        self._unlike(request.user_data, pk)

        payload = {"page_id": pk, "type": "unlike"}
        kafka_producer.produce_message("posts", payload)

        return Response(data={"detail": "Post is unliked."})

    def _like(self, user_data, pk):
        likes = Likes.objects.filter(post_id=pk, user=user_data.get("uuid"))
        if not likes:
            likes = Likes.objects.create(post_id=pk, user=user_data.get("uuid"))

        return likes

    def _unlike(self, user_data, pk):
        Likes.objects.filter(post_id=pk, user=user_data.get("uuid")).delete()


class Feed(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        followers = Followers.objects.filter(
            user=request.user_data.get("uuid")
        ).select_related("page")
        posts = Post.objects.filter(page__follows__in=followers)

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)
