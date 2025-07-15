from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated

from company.models import CompanyRoleUser
from company.permissions import AnyCompanyRolePermissions, CompanyPermissions
from core.base.responses import ResponseException
from core.base.views import BaseAPIView
from guidebook.filters import GuideBookFilter, WorkFilter
from guidebook.models import GuideBook, Work
from guidebook.paginators import Pagination
from guidebook.permissions import (
    CheckingUserIsAuthorInCompany,
    CheckingUserWorkInCompany,
)
from guidebook.responses_schema_config import GuideBookResponse, WorkResponse
from guidebook.serializers import (
    DirectoryWithEmbeddedDataOutputSerializer,
    EnteringDirectoryDataInputSerializer,
    ViewingDirectoryOnlyNameOutputSerializer,
    ViewingGuideBookOutputSerializer,
    WorkDataInputSerializer,
    WorkDataOutputSerializer,
)
from guidebook.service import GuideBookService, WorkService


class GuideBooksListView(BaseAPIView):
    """вью просмотра списка справочников"""

    output_serializer_class = ViewingDirectoryOnlyNameOutputSerializer
    permission_classes = [IsAuthenticated, AnyCompanyRolePermissions]
    pagination_class = Pagination
    filter_backends = [GuideBookFilter]
    guidebook_list: [QuerySet[GuideBook]] = None

    def initial(self, request, *args, **kwargs):
        self.guidebook_list = GuideBookService.get_guidebook_parents(
            kwargs["pk_company"]
        )
        if not self.guidebook_list:
            raise ResponseException(
                self.response_404(message="Справочники не найдены.")
            )
        return super().initial(request, *args, **kwargs)

    @GuideBookResponse.list_guidebooks
    def get(self, request, *args, **kwargs):
        queryset = self.guidebook_list
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.output_serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class GuideBookCreateView(BaseAPIView):
    """вью создания справочника, функция доступна только пользователю с ролью author"""

    input_serializer_class = EnteringDirectoryDataInputSerializer
    output_serializer_class = ViewingGuideBookOutputSerializer
    permission_classes = [IsAuthenticated, CompanyPermissions]
    required_roles = [
        CompanyRoleUser.RoleType.AUTHOR,
    ]

    @GuideBookResponse.create_guidebook
    def post(self, request, *args, **kwargs):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        guidebook = GuideBookService.create_guidebook(
            kwargs["pk_company"], **input_serializer.validated_data
        )
        output_serializer = self.output_serializer_class(guidebook)

        return self.response_201(output_serializer.data)


class GuideBookDetailView(BaseAPIView):
    """вью просмотра детально одного справочника"""

    output_serializer_class = DirectoryWithEmbeddedDataOutputSerializer
    permission_classes = [IsAuthenticated, CheckingUserWorkInCompany]

    @GuideBookResponse.one_guidebook
    def get(self, request, *args, **kwargs):
        construction_guidebook = GuideBookService.get_guidebook(kwargs["pk_guidebook"])
        if construction_guidebook is None:
            return self.response_404()
        construction_guidebook_data = ViewingDirectoryOnlyNameOutputSerializer(
            construction_guidebook
        ).data

        nested_guidebooks = GuideBookService.list_guidebook(kwargs["pk_guidebook"])
        nested_guidebooks_data = ViewingDirectoryOnlyNameOutputSerializer(
            nested_guidebooks, many=True
        ).data

        nested_works = WorkService.get_works_by_pk_guidebook(kwargs["pk_guidebook"])
        nested_works_data = WorkDataOutputSerializer(nested_works or [], many=True).data

        serializer = self.output_serializer_class(
            data={
                "guidebook": construction_guidebook_data,
                "nested_guidebooks": nested_guidebooks_data,
                "nested_works": nested_works_data,
            }
        )

        serializer.is_valid(raise_exception=True)

        return self.response_200(data=serializer.validated_data)


class GuideBookUpdateDeliteView(BaseAPIView):
    """вью обновления и мягкого удаления справочника, доступно author"""

    input_serializer_class = EnteringDirectoryDataInputSerializer
    output_serializer_class = ViewingGuideBookOutputSerializer
    permission_classes = [IsAuthenticated, CheckingUserIsAuthorInCompany]
    guidebook: GuideBook = None

    def initial(self, request, *args, **kwargs):
        self.guidebook = GuideBookService.get_guidebook(kwargs["pk_guidebook"])
        if self.guidebook is None:
            raise ResponseException(self.response_404(message="Справочник не найден."))
        return super().initial(request, *args, **kwargs)

    @GuideBookResponse.soft_delete_guidebook
    def delete(self, request, *args, **kwargs):
        GuideBookService.soft_delete_get_object_by_model(self.guidebook)
        return self.response_204()

    @GuideBookResponse.update_guidebook
    def put(self, request, *args, **kwargs):
        input_serializer = EnteringDirectoryDataInputSerializer(
            instance=self.guidebook, data=request.data
        )
        input_serializer.is_valid(raise_exception=True)
        guidebook = GuideBookService.update_guidebook(
            self.guidebook, **input_serializer.validated_data
        )
        return self.response_200(ViewingGuideBookOutputSerializer(guidebook).data)


# Работы


class WorkListView(BaseAPIView):
    """вью просмотра списка работ"""

    output_serializer_class = WorkDataOutputSerializer
    permission_classes = [IsAuthenticated, CheckingUserWorkInCompany]
    pagination_class = Pagination
    filter_backends = [WorkFilter]
    work_list: [QuerySet[Work]] = None

    def initial(self, request, *args, **kwargs):
        self.work_list = WorkService.get_works_by_pk_guidebook(kwargs["pk_guidebook"])
        if self.work_list is None:
            raise ResponseException(
                self.response_404(message="Работы в справочнике не найдены.")
            )
        return super().initial(request, *args, **kwargs)

    @WorkResponse.list_works
    def get(self, request, *args, **kwargs):
        queryset = self.work_list
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.output_serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


class WorkCreateView(BaseAPIView):
    """вью создания работы, функция доступна только пользователю с ролью author"""

    input_serializer_class = WorkDataInputSerializer
    output_serializer_class = WorkDataOutputSerializer
    permission_classes = [IsAuthenticated, CheckingUserIsAuthorInCompany]

    @WorkResponse.create_work
    def post(self, request, *args, **kwargs):
        input_serializer = self.input_serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        work = WorkService.create_work(**input_serializer.validated_data)
        output_serializer = self.output_serializer_class(work)

        return self.response_201(output_serializer.data)


class WorkDetailView(BaseAPIView):
    """вью просмотра детально одной работы"""

    output_serializer_class = WorkDataOutputSerializer
    permission_classes = [IsAuthenticated, CheckingUserWorkInCompany]

    @WorkResponse.one_work
    def get(self, request, *args, **kwargs):
        work = WorkService.get_work(kwargs["pk_work"])
        if work is None:
            return self.response_404()
        return self.response_200(self.output_serializer_class(work).data)


class WorkUpdateAndDeliteView(BaseAPIView):
    """вью обновления работы, доступно author"""

    input_serializer_class = WorkDataInputSerializer
    output_serializer_class = WorkDataOutputSerializer
    permission_classes = [
        IsAuthenticated,
        CheckingUserIsAuthorInCompany,
    ]
    work: Work = None

    def initial(self, request, *args, **kwargs):
        self.work = WorkService.get_work(kwargs["pk_work"])
        if self.work is None:
            raise ResponseException(self.response_404(message="Работа не найдена."))
        return super().initial(request, *args, **kwargs)

    @WorkResponse.update_work
    def put(self, request, *args, **kwargs):
        input_serializer = WorkDataInputSerializer(
            instance=self.work, data=request.data
        )
        input_serializer.is_valid(raise_exception=True)
        work = WorkService.update_work(self.work, **input_serializer.validated_data)
        return self.response_200(WorkDataOutputSerializer(work).data)

    @WorkResponse.soft_delete_work
    def delete(self, request, *args, **kwargs):
        WorkService.soft_delete_get_object_by_model(self.work)
        return self.response_204()
