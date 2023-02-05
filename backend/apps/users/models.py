from apps.users.managers import UserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    A model which implements an authentication model.
    Email and password are required. Other fields are optional.
    Email field is being used for logging in.
    """

    email = models.EmailField(_("Email address"), unique=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
