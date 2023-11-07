from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, code):
        super().__init__(detail, code)
        self.detail = detail
        self.status_code = code


class AlreadyFollowerException(BaseCustomException):
    def __init__(self):
        detail = "You are already a follower."
        super().__init__(detail, status.HTTP_422_UNPROCESSABLE_ENTITY)


class PageDoesNotExistException(BaseCustomException):
    def __init__(self):
        detail = "The page does not exist."
        super().__init__(detail, status.HTTP_422_UNPROCESSABLE_ENTITY)


class NotAFollowerException(BaseCustomException):
    def __init__(self):
        detail = "You are not a follower."
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)
