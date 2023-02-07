from apps.events.models import Event, EventType
from django.contrib import admin


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """A class to register EventType model at admin panel."""

    list_display = ("id", "name")
    list_display_links = ("id", "name")
    list_per_page = 25


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """A class to register Event model at admin panel."""

    list_display = ("id", "user", "event_type", "info", "timestamp", "created_at")
    list_display_links = ("id",)
    list_filter = ("event_type", "timestamp")
    list_per_page = 25
    raw_id_fields = ("user", "event_type")
    readonly_fields = ("created_at",)
