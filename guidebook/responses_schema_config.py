from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers

from core.base.responses_schema_config import BaseResponsesConfig
from guidebook.serializers import (
    DirectoryWithEmbeddedDataOutputSerializer,
    EnteringDirectoryDataInputSerializer,
    ViewingDirectoryOnlyNameOutputSerializer,
    ViewingGuideBookOutputSerializer,
    WorkDataInputSerializer,
    WorkDataOutputSerializer,
)


class GuideBookResponse(BaseResponsesConfig):
    """Класс с документацией для справочнике"""

    one_guidebook = extend_schema(
        summary="Получить полную информацию о справочнике",
        description="Возвращает детальную информацию о справочнике.",
        responses={
            200: DirectoryWithEmbeddedDataOutputSerializer,
            403: OpenApiResponse(description="Справочник не найден"),
        },
        tags=["Справочники"],
    )

    update_guidebook = extend_schema(
        summary="Обновить информацию о справочнике",
        description="Обновляет данные справочника.<br>" "Доступно владельцу компании.",
        request=EnteringDirectoryDataInputSerializer,
        responses={
            200: ViewingGuideBookOutputSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            403: OpenApiResponse(
                description="Справочник не найден или нет ролей в компании"
            ),
        },
        tags=["Справочники"],
    )

    create_guidebook = extend_schema(
        summary="Создать новый справочник",
        description="Создаёт новый справочник, pk компании передается в ссылке.<br>"
        "Доступно владельцу компании.",
        request=EnteringDirectoryDataInputSerializer,
        responses={
            201: ViewingGuideBookOutputSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=["Справочники"],
    )

    soft_delete_guidebook = extend_schema(
        summary="Мягкое удаление справочника",
        description="Удаляет справочник.<br>" "Доступно только владельцу компании.",
        responses={
            204: OpenApiResponse(description="Справочник удален"),
            403: OpenApiResponse(
                description="Справочник не найден или нет ролей в компании"
            ),
        },
        tags=["Справочники"],
    )

    list_guidebooks = extend_schema(
        summary="Получить список объектов",
        description="Получает список объектов компании, pk компании передается в ссылке.<br>"
        "Параметры запроса позволяют фильтровать и сортировать результаты.",
        responses={
            200: inline_serializer(
                name="CityListResponse",
                fields={
                    "count": serializers.IntegerField(),
                    "next": serializers.CharField(allow_null=True),
                    "previous": serializers.CharField(allow_null=True),
                    "results": ViewingDirectoryOnlyNameOutputSerializer(many=True),
                },
            ),
            404: OpenApiResponse(description="Не найдено"),
        },
        parameters=[
            OpenApiParameter(
                name="page",
                required=False,
                description="Номер страницы (по умолчанию 1)",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="page_size",
                required=False,
                description="Количество элементов на странице (по умолчанию 10)",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="title",
                required=False,
                description="Поиск по названию объекта (регистр игнорируется)",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ],
        tags=["Справочники"],
    )


class WorkResponse(BaseResponsesConfig):
    """Класс с документацией для справочнике"""

    one_work = extend_schema(
        summary="Получить полную информацию о справочнике",
        description="Возвращает детальную информацию о справочнике.",
        responses={
            200: ViewingGuideBookOutputSerializer,
            403: OpenApiResponse(description="Справочник не найден"),
        },
        tags=["Работы"],
    )

    update_work = extend_schema(
        summary="Обновить информацию о работе",
        description="Обновляет данные работы.<br>" "Доступно владельцу компании.",
        request=WorkDataInputSerializer,
        responses={
            200: WorkDataOutputSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            403: OpenApiResponse(
                description="Работа не найдена или нет ролей в компании"
            ),
        },
        tags=["Работы"],
    )

    create_work = extend_schema(
        summary="Создать новую работу",
        description="Создаёт новую работу.<br>" "Доступно владельцу компании.",
        request=WorkDataInputSerializer,
        responses={
            201: WorkDataOutputSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=["Работы"],
    )

    soft_delete_work = extend_schema(
        summary="Мягкое удаление работы",
        description="Удаляет работу.<br>" "Доступно только владельцу компании.",
        responses={
            204: OpenApiResponse(description="Работа удалена"),
            403: OpenApiResponse(
                description="Работа не найдена или нет ролей в компании"
            ),
        },
        tags=["Работы"],
    )

    list_works = extend_schema(
        summary="Получить список работ",
        description="Получает список работ компании, pk компании передается в ссылке.<br>"
        "Параметры запроса позволяют фильтровать и сортировать результаты.",
        responses={
            200: inline_serializer(
                name="CityListResponse",
                fields={
                    "count": serializers.IntegerField(),
                    "next": serializers.CharField(allow_null=True),
                    "previous": serializers.CharField(allow_null=True),
                    "results": ViewingDirectoryOnlyNameOutputSerializer(many=True),
                },
            ),
            404: OpenApiResponse(description="Не найдено"),
        },
        parameters=[
            OpenApiParameter(
                name="page",
                required=False,
                description="Номер страницы (по умолчанию 1)",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="page_size",
                required=False,
                description="Количество элементов на странице (по умолчанию 10)",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="title",
                required=False,
                description="Поиск по названию объекта (регистр игнорируется)",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ],
        tags=["Работы"],
    )
