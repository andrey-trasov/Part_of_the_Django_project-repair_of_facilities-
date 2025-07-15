from django.db import models

from core.base.models import BaseModel

NULLABLE = {"blank": True, "null": True}


class GuideBook(BaseModel):
    """базовая модель справочника"""

    company = models.ForeignKey(
        "company.Company",
        on_delete=models.CASCADE,
        related_name="guidebooks",
        verbose_name="Компания",
        db_default=None,
    )
    title = models.CharField(
        max_length=150, verbose_name="Название справочника", db_default=None
    )
    parent_guide_book = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children_guide_book",
        verbose_name="Родительский справочник",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        result = f"СПРАВОЧНИК-{self.title}, КОМПАНИИ-{self.company.name}"
        return result


class Work(BaseModel):
    """базовая модель работы"""

    class UnitType(models.TextChoices):
        """Единицы измерения"""

        CUBIC_METER = "cubic_meter", "Кубический метр"
        SQUARE_METER = "square_meter", "Квадратный метр"
        LINEAR_METER = "linear_meter", "Погонный метр"

    class CurrencyType(models.TextChoices):
        """Валюта"""

        RUB = "rub", "Рубль"
        USD = "usd", "Доллар США"
        EUR = "eur", "Евро"

    guidebook = models.ForeignKey(
        "GuideBook",
        on_delete=models.CASCADE,
        related_name="works",
        verbose_name="Справочник",
        db_default=None,
    )
    title = models.CharField(
        max_length=150, verbose_name="Название работы", db_default=None
    )
    price_by_unit = models.IntegerField(
        verbose_name="Цена за одну единицу", db_default=None
    )
    unit_of_measurement = models.CharField(
        choices=UnitType,
        default=UnitType.LINEAR_METER,
        max_length=20,
        verbose_name="Единица измерения",
        db_default=None,
    )
    currency = models.CharField(
        choices=CurrencyType,
        default=CurrencyType.RUB,
        max_length=3,
        verbose_name="Валюта",
        db_default=None,
    )

    class Meta:
        verbose_name = "Работа в справочнике"
        verbose_name_plural = "Работы в справочнике"

    def __str__(self):
        result = (
            f"РАБОТА-{self.title} В СПРАВОЧНИКЕ-{self.guidebook.title}, "
            f"КОМПАНИИ-{self.guidebook.company.name}"
        )
        return result
