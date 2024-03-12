from rest_framework.pagination import PageNumberPagination


class CategoriesPagination(PageNumberPagination):
    page_size = 10


class ProductsPagination(PageNumberPagination):
    page_size = 10