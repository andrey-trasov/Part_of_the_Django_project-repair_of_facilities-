from django.urls import path

from guidebook.apps import GuidebookConfig

from .views import (
    GuideBookCreateView,
    GuideBookDetailView,
    GuideBooksListView,
    GuideBookUpdateDeliteView,
    WorkCreateView,
    WorkDetailView,
    WorkListView,
    WorkUpdateAndDeliteView,
)

app_name = GuidebookConfig.name

urlpatterns = [
    # справочники
    path(
        "guidebook_list/<int:pk_company>/",
        GuideBooksListView.as_view(),
        name="guidebook_list/pk_company",
    ),
    path(
        "<int:pk_guidebook>/",
        GuideBookDetailView.as_view(),
        name="pk_guidebook",
    ),
    path(
        "guidebook_create/<int:pk_company>/",
        GuideBookCreateView.as_view(),
        name="guidebook_create/pk_company",
    ),
    path(
        "change/<int:pk_guidebook>/",
        GuideBookUpdateDeliteView.as_view(),
        name="change/pk_guidebook",
    ),
    # работы
    path(
        "work_list/<int:pk_guidebook>/",
        WorkListView.as_view(),
        name="work_list/pk_guidebook",
    ),
    path("work/<int:pk_work>/", WorkDetailView.as_view(), name="pk_work"),
    path("work_create/", WorkCreateView.as_view(), name="work_create"),
    path(
        "change_work/<int:pk_work>/",
        WorkUpdateAndDeliteView.as_view(),
        name="change_work/pk_work",
    ),
]
