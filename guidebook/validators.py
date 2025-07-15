from rest_framework import serializers

from guidebook.models import GuideBook


class GuideBookValidator:
    """Проверяет существование справочника по ID"""

    def __call__(self, value):
        try:
            # Проверяем, существует ли справочник с данным ID
            guidebook = GuideBook.objects.get(id=value)
            return guidebook
        except GuideBook.DoesNotExist:
            raise serializers.ValidationError("Справочник с таким ID не найдена.")
