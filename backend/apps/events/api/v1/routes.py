from apps.events.api.v1.views import ListCreateEventAPIView
from django.urls import path

app_name = "events"
urlpatterns = [
    path("", ListCreateEventAPIView.as_view(), name="event_list"),
]
