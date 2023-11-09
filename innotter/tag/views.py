from page.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Tag
from .pagination import PageNumberOffsetPagination
from .serializer import TagSerializer


class TagViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberOffsetPagination
    permission_classes_by_action = {
        "create": [IsAuthenticated],
        "list": [IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        name = self.request.query_params.get("filter_by_name")
        if not name:
            return super().get_queryset()

        return Tag.objects.filter(name__icontains=name)
