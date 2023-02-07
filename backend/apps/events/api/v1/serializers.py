from apps.events.models import Event, EventType
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    """A serializer class for Event model."""

    user_id = serializers.PrimaryKeyRelatedField(source="user", read_only=True)
    event_type = serializers.CharField(max_length=256)

    def create(self, validated_data):
        """
        Create a new EventType and Event instances if they do NOT exist yet.
        Return Event.
        """

        name = validated_data.pop("event_type")
        event_type = EventType.objects.filter(name=name).first()
        if not event_type:
            event_type = EventType.objects.create(name=name)

        validated_data.update(event_type=event_type)

        event = Event.objects.filter(**validated_data).first()
        if not event:
            event = super().create(validated_data=validated_data)
        return event

    class Meta:
        model = Event
        fields = ("user_id", "event_type", "info", "timestamp", "created_at")
        read_only_fields = ("created_at",)
