from random import choice

from apps.events.models import Event, EventType
from django.conf import settings
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

UserModel = get_user_model()
fake = Faker()
timestamp_format = settings.REST_FRAMEWORK.get("DATETIME_INPUT_FORMATS")[0]


class TestEventListView(APITestCase):
    """Class for testing event list api endpoint."""

    def setUp(self):
        """Called before each single test. Creates 1 user, 2 event types and 5 events."""

        self.user = UserModel.objects.create(email=fake.email(), password=fake.password())

        event_types = []
        for i in range(2):
            event_types.append(EventType.objects.create(name=fake.word()))

        for i in range(5):
            Event.objects.create(
                user=self.user,
                event_type=choice(event_types),
                info=fake.json(),
                timestamp=fake.date_time(),
            )

        self.event_list_url = reverse("events:event_list")
        self.client.force_authenticate(user=self.user)

    def test_get_events(self):
        """Ensure any user can get an event list."""

        # anonymous user
        self.client.force_authenticate(user=None)
        response = self.client.get(self.event_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), 5)

        # authorized user
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.event_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 5)

    def test_create_event_non_authorized(self):
        """Ensure unauthorized user can NOT create a new event."""

        self.client.force_authenticate(user=None)
        response = self.client.post(
            path=self.event_list_url,
            data={
                "event_type": fake.word(),
                "info": fake.json(),
                "timestamp": fake.date_time(tzinfo=None).strftime(timestamp_format),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Event.objects.count(), 5)

    def test_create_event_authorized(self):
        """Ensure authorized user can create a new event."""

        response = self.client.post(
            path=self.event_list_url,
            data={
                "event_type": fake.word(),
                "info": fake.json(),
                "timestamp": fake.date_time(tzinfo=None).strftime(timestamp_format),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 6)

    def test_create_event_authorized_missing_data(self):
        """Ensure authorized user can NOT create a new event with the missing data."""

        response = self.client.post(
            path=self.event_list_url,
            data={
                "event_type": fake.word(),
                "info": fake.json(),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 5)

    def test_create_event_authorized_wrong_data(self):
        """Ensure authorized user can NOT create a new event with the wrong data."""

        response = self.client.post(
            path=self.event_list_url,
            data={
                "event_type": fake.word(),
                "info": fake.json(),
                "timestamp": fake.date_time(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.count(), 5)
