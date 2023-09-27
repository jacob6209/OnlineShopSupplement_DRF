from rest_framework.pagination import PageNumberPagination

class DefultPagination(PageNumberPagination):
    page_size=10
    