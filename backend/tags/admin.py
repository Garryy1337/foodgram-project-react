from django.contrib import admin

from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "color", "slug")
    search_fields = ("name",)
    empty_value_display = "-пусто-"
