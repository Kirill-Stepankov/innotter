from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class ListUsers(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response(request.user_data)
