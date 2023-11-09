from rest_framework.pagination import PageNumberPagination


class PageNumberOffsetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "offset"
    max_page_size = 100
