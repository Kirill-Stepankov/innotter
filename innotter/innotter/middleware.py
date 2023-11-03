import requests
from django.http import JsonResponse

from .settings import env


class AuthServiceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get("token")

        user_data = None
        if not token:
            request.user_data = user_data
            return self.get_response(request)

        resp = requests.get(env("AUTH_ENDPOINT"), headers={"token": token})

        if resp.status_code != 200:
            return JsonResponse(data=resp.json(), status=resp.status_code)

        request.user_data = resp.json()
        return self.get_response(request)
