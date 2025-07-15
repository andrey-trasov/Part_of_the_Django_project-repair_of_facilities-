from rest_framework import permissions

from company.models import CompanyRoleUser
from guidebook.models import GuideBook, Work


class CheckingUserWorkInCompany(permissions.BasePermission):
    """
    Проверяет, работает ли пользователь в компании которой принадлежит справочник или работа из справочника.
    Пермишен может работать сразу с двумя кварками `pk_work` и `pk_guidebook`
    Если проверка не пройдена, вернет ошибку 403.
    """

    def has_permission(self, request, view):
        pk_work = view.kwargs.get("pk_work", None)
        if pk_work is not None:
            work = Work.objects.filter(id=pk_work).first()
            pk_guidebook = work.guidebook_id
        else:
            pk_guidebook = view.kwargs.get("pk_guidebook", None)
        guidebook = GuideBook.objects.filter(id=pk_guidebook).first()

        result: bool = CompanyRoleUser.objects.filter(
            user=request.user, company_id=guidebook.company_id
        ).exists()

        return result


class CheckingUserIsAuthorInCompany(permissions.BasePermission):
    """
    Проверяет, имеет ли пользователь роль "author" в компании которой принадлежит справочник или работа из справочника.
    Пермишен может работать сразу с двумя кварками `pk_work` и `pk_guidebook` и data "guidebook".
    Если проверка не пройдена, вернет ошибку 403.
    """

    def has_permission(self, request, view):
        pk_work = view.kwargs.get("pk_work", None)
        if pk_work is not None:
            work = Work.objects.filter(id=pk_work).first()
            pk_guidebook = work.guidebook_id
        else:
            pk_guidebook = request.data.get("guidebook", None)
            if pk_guidebook is None:
                pk_guidebook = view.kwargs.get("pk_guidebook", None)

        guidebook = GuideBook.objects.filter(id=pk_guidebook).first()

        result: bool = CompanyRoleUser.objects.filter(
            user=request.user, company_id=guidebook.company_id, role="author"
        ).exists()

        return result
