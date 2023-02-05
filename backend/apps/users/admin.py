from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.admin import TokenAdmin

UserModel = get_user_model()

TokenAdmin.raw_id_fields = ["user"]


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    """A class to represent the user at admin panel."""

    list_display = ("id", "email", "date_joined", "last_login", "is_staff")
    list_display_links = ("id", "email")
    search_fields = ("email",)
    readonly_fields = ("date_joined", "last_login", "is_staff")
    ordering = ("id",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
