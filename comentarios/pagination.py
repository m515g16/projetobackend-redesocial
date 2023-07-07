from rest_framework.pagination import PageNumberPagination


class PaginationCustomer(PageNumberPagination):
    page_size = 25
    max_page_size = 50
