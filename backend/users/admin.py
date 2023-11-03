from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Регистрируем подписку в админке."""

    list_display = ("id", "user", "author")
    search_fields = ("user", "author")
    empty_value_display = "-пусто-"
