from rest_framework.pagination import PageNumberPagination


class PublicationUserPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 20
