from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user creation endpoint."""

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """Create a new user and a token for this User."""

        user = UserModel.objects.create_user(
            email=validated_data.get("email"),
            password=validated_data.get("password"),
        )

        return user

    class Meta:
        model = UserModel
        fields = ("email", "password")


class CustomAuthTokenSerializer(serializers.Serializer):
    """Serializer for obtaining auth token endpoint."""

    email = serializers.EmailField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_(
            "Password",
        ),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        """Ensure user with the provided credentials exists."""

        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"), email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
