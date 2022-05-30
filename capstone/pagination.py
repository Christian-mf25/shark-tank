from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "per_page"
    max_page_size = 100
