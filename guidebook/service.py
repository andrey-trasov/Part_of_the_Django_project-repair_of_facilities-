from typing import Union

from django.db.models import QuerySet

from core.base.service import BaseService
from guidebook.models import GuideBook, Work


class GuideBookService(BaseService):
    """операции со справочниками"""

    @classmethod
    def get_guidebook_parents(cls, pk_company: int) -> Union[QuerySet[GuideBook], None]:
        """функция для получения справочников по pk_guidebook и parent_guide_book = None"""
        guidebooks = (
            GuideBook.objects.filter(company_id=pk_company, parent_guide_book=None)
            .all()
            .order_by("id")
        )
        if not guidebooks.exists():
            return None
        return guidebooks

    @classmethod
    def get_guidebook(cls, pk: int) -> Union[GuideBook, None]:
        """функция для получения справочника по pk_guidebook"""
        return cls.get_object_by_model(GuideBook, pk)

    @classmethod
    def list_guidebook(cls, pk: int) -> QuerySet[GuideBook]:
        """функция получения списка справочников по pk_guidebook родителя"""
        guidebooks = GuideBook.objects.filter(parent_guide_book=pk)
        return guidebooks

    @classmethod
    def create_guidebook(cls, pk_company: int, **kwargs) -> GuideBook:
        """функция создания справочника"""
        guidebook = GuideBook.objects.create(
            company_id=pk_company,
            title=kwargs.get("title"),
            parent_guide_book_id=kwargs.get("parent_guide_book"),
        )
        return guidebook

    @classmethod
    def update_guidebook(cls, guidebook: GuideBook, **kwargs) -> GuideBook:
        """функция обновления справочника"""
        guidebook.company_id = kwargs.get("company", guidebook.company_id)
        guidebook.title = kwargs.get("title", guidebook.title)
        guidebook.parent_guide_book = kwargs.get(
            "parent_guide_book", guidebook.parent_guide_book
        )

        guidebook.save()
        return guidebook


class WorkService(BaseService):
    """операции с работами"""

    @classmethod
    def get_work(cls, pk: int) -> Union[Work, None]:
        """функция для получения работы по pk_work"""
        return cls.get_object_by_model(Work, pk)

    @classmethod
    def get_works_by_pk_guidebook(
        cls, pk_guidebook: int
    ) -> Union[QuerySet[Work], None]:
        """функция получения списка работ внутри справочника."""
        works = Work.objects.filter(guidebook_id=pk_guidebook)
        if not works.exists():
            return None
        return works

    @classmethod
    def create_work(cls, **kwargs) -> Work:
        """функция создания работы"""
        work = Work.objects.create(
            guidebook_id=kwargs.get("guidebook"),
            title=kwargs.get("title"),
            price_by_unit=kwargs.get("price_by_unit"),
            unit_of_measurement=kwargs.get("unit_of_measurement"),
            currency=kwargs.get("currency"),
        )
        return work

    @classmethod
    def update_work(cls, work: Work, **kwargs) -> Work:
        """функция обновления работы"""
        work.guidebook_id = kwargs.get("guidebook", work.guidebook_id)
        work.title = kwargs.get("title", work.title)
        work.price_by_unit = kwargs.get("price_by_unit", work.price_by_unit)
        work.unit_of_measurement = kwargs.get(
            "unit_of_measurement", work.unit_of_measurement
        )
        work.currency = kwargs.get("currency", work.currency)
        work.save()
        return work
