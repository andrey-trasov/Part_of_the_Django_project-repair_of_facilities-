from rest_framework import filters


class GuideBookFilter(filters.BaseFilterBackend):
    """
    Кастомный фильтр, фильтрует по полю title.
    Возвращает только справочники первого порядка "parent_guide_book=None"
    """

    def filter_queryset(self, request, queryset, view):
        search_param_1 = request.query_params.get("title", None)
        if search_param_1:
            queryset = queryset.filter(title__icontains=search_param_1.lower())

        return queryset.order_by("id")


class WorkFilter(filters.BaseFilterBackend):
    """
    Кастомный фильтр, фильтрует по полю title.
    Возвращает список работ по pk справочника
    """

    def filter_queryset(self, request, queryset, view):
        search_param_1 = request.query_params.get("title", None)
        if search_param_1:
            queryset = queryset.filter(
                title__icontains=search_param_1.lower(),
            )

        return queryset.order_by("id")
