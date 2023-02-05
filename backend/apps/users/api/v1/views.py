from apps.users.api.v1.serializers import CustomAuthTokenSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

UserModel = get_user_model()


class UserCreateAPIView(CreateAPIView):
    """View for creating a new user."""

    model = UserModel
    permissions = [permissions.AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        """
        Create a new user with the provided email and password.
        And generate a new token for this user.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)

        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class CustomAuthTokenAPIView(APIView):
    """View for obtaining an auth token."""

    def post(self, request, *args, **kwargs):
        """
        Create a token for a user. Return a token if it already exists.
        """

        serializer = CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        token, created = Token.objects.get_or_create(user=user)

        if created:
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
