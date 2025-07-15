from django.contrib import admin

from guidebook.models import GuideBook, Work


@admin.register(GuideBook)
class GuideBookAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "title", "parent_guide_book",)
    list_filter = ("company",)
    search_fields = ("company",)
    fields = ("company", "title", "parent_guide_book",)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "guidebook",)
    list_filter = ("guidebook",)
    search_fields = ("title",)
    fields = ("guidebook",
              "title",
              "unit_of_measurement",
              "price_by_unit",
              "currency",)
