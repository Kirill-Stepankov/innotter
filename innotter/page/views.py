from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Page
from .permissions import (
    IsAdmin,
    IsAdminOrIsOwnerOrIsModeratorOfTheOwner,
    IsAuthenticated,
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

    # переоперделить retrieve
    # добавить экшены
