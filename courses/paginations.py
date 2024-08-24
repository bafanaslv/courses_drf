from rest_framework.pagination import PageNumberPagination


class CoursesPaginator(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 10


class LessionsPaginator(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 10
