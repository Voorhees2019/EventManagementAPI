from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class EventType(models.Model):
    """A model to represent an event type."""

    name = models.CharField(_("Name"), max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Event Type")
        verbose_name_plural = _("Event Types")


class Event(models.Model):
    """A model to represent an event."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="user_events")
    event_type = models.ForeignKey(
        to=EventType,
        on_delete=models.SET_NULL,
        related_name="events",
        blank=True,
        null=True,
    )
    info = models.JSONField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ("-created_at",)

    def __str__(self):
        return f"Event {self.id}"
