import logging

import requests
from django.http import JsonResponse

from .settings import env

logger = logging.getLogger(__name__)


class AuthServiceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get("token")

        user_data = None
        if not token:
            request.user_data = user_data
            return self.get_response(request)

        logger.info("Requesting user data...")
        resp = requests.get(env("AUTH_ENDPOINT"), headers={"token": token})

        if resp.status_code != 200:
            logger.info("The request failed")
            return JsonResponse(data=resp.json(), status=resp.status_code)

        logger.info("The request is successful")
        request.user_data = resp.json()
        return self.get_response(request)
