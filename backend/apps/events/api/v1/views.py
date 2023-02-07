from apps.events.api.v1.serializers import EventSerializer
from apps.events.models import Event
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


class ListCreateEventAPIView(generics.ListCreateAPIView):
    """
    LIST / CREATE view for Event model.

    API
    -----------
    GET:
        Return a list of Events.
    POST:
        Create and return a new Event instance.
    """

    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Event.objects.all()

    def get(self, request, *args, **kwargs):
        """Get a list of events."""

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create a new event with the provided data."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
