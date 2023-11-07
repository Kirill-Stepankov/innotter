from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .exceptions import (
    AlreadyFollowerException,
    NotAFollowerException,
    PageDoesNotExistException,
)
from .models import Followers, Page
from .permissions import (
    IsAdmin,
    IsAdminOrIsOwnerOrIsModeratorOfTheOwner,
    IsAuthenticated,
    IsModeratorOfThePageOwner,
    IsPageOwner,
)
from .serializer import PageSerializer
from .utils import upload_file_s3


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes_by_action = {
        "create": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "update": [IsPageOwner],
        "partial_update": [IsPageOwner],
        "destroy": [IsAdminOrIsOwnerOrIsModeratorOfTheOwner],
        "list": [IsAuthenticated],
    }

    def perform_update(self, serializer):
        key = serializer.validated_data.get("name") or self.get_object().name
        key = self._upload_file(key, serializer)

        serializer.save(image=key)

    def perform_create(self, serializer):
        # add logger
        key = None
        key = self._upload_file(key, serializer)

        serializer.save(
            owner=self.request.user_data.get("uuid"),
            owner_group_id=self.request.user_data.get("group_id"),
            image=key,
        )

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        self._follow(pk, request.user_data)
        return Response(
            data={"detail": "Successfully followed"}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        self._unfollow(pk, request.user_data)
        return Response(
            data={"detail": "Successfully unfollowed"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsAdminOrIsOwnerOrIsModeratorOfTheOwner],
    )
    def followers(self, request, pk=None):
        pass

    @action(
        detail=True, methods=["patch"], permission_classes=[IsModeratorOfThePageOwner]
    )
    def block(self, request, pk=None):
        pass

    @action(detail=True, methods=["post"], permission_classes=[IsPageOwner])
    def post(self, request, pk=None):
        # сериализатор и тд
        pass

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def _upload_file(self, key, serializer):
        file = self.request.FILES.get("picture")
        if file:
            key = serializer.validated_data.get("name") or key
            raw_data = file.read()
            upload_file_s3(raw_data, key)

        return key

    def _follow(self, pk, user_data):
        page = Page.objects.filter(pk=pk).all()
        if not page:
            raise PageDoesNotExistException

        followers = Followers.objects.filter(
            post_id=pk, user=user_data.get("uuid")
        ).all()
        if followers:
            raise AlreadyFollowerException

        followers = Followers(post_id=pk, user=user_data.get("uuid"))
        followers.save()

    def _unfollow(self, pk, user_data):
        page = Page.objects.filter(pk=pk).all()
        if not page:
            raise PageDoesNotExistException

        followers = Followers.objects.filter(
            post_id=pk, user=user_data.get("uuid")
        ).all()
        if not followers:
            raise NotAFollowerException

        followers.delete()

    # переоперделить retrieve
    # добавить экшены
