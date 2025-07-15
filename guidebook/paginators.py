from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 10  # количество сущностей на 1 странице
    page_size_query_param = (
        "page_size"  # количество выведенных записей (вводит пользователь)
    )
    max_page_size = 10  # максимальное количество сущностей на 1 странице
