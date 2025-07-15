from rest_framework import serializers

from company.serializers import CompanyOutputSerializer
from guidebook.validators import GuideBookValidator

# СПРАВОЧНИК


class ViewingDirectoryOnlyNameOutputSerializer(serializers.Serializer):
    """сериализатор для просмотра справочниа, только название"""

    id = serializers.IntegerField()
    title = serializers.CharField()


class EnteringDirectoryDataInputSerializer(serializers.Serializer):
    """сериализатор ввода данных справочника"""

    title = serializers.CharField()
    parent_guide_book = serializers.IntegerField(
        validators=[GuideBookValidator()], required=False
    )


class ViewingGuideBookOutputSerializer(serializers.Serializer):
    """сериализатор для просмотра справочника"""

    id = serializers.IntegerField()
    company = CompanyOutputSerializer()
    title = serializers.CharField()
    parent_guide_book = ViewingDirectoryOnlyNameOutputSerializer()


class WorkOutputSerializer(serializers.Serializer):
    """сериализатор для просмотра работы"""

    id = serializers.IntegerField()
    title = serializers.CharField()
    price_by_unit = serializers.IntegerField()
    unit_of_measurement = serializers.CharField()
    currency = serializers.CharField()


class DirectoryWithEmbeddedDataOutputSerializer(serializers.Serializer):
    """сериализатор для вывода справочника с влоденными справочниками и работами"""

    guidebook = ViewingDirectoryOnlyNameOutputSerializer()
    nested_guidebooks = ViewingDirectoryOnlyNameOutputSerializer(many=True)
    nested_works = WorkOutputSerializer(many=True)


# РАБОТА


class WorkDataInputSerializer(serializers.Serializer):
    """сериализатор ввода данных работы"""

    guidebook = serializers.IntegerField(validators=[GuideBookValidator()])
    title = serializers.CharField(max_length=150)
    price_by_unit = serializers.IntegerField(min_value=0)
    unit_of_measurement = serializers.CharField()
    currency = serializers.CharField()


class WorkDataOutputSerializer(serializers.Serializer):
    """сериализатор для просмотра работы"""

    id = serializers.IntegerField()
    guidebook = ViewingDirectoryOnlyNameOutputSerializer()
    title = serializers.CharField()
    price_by_unit = serializers.IntegerField()
    unit_of_measurement = serializers.CharField()
    currency = serializers.CharField()
