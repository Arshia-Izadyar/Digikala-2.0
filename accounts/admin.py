from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("email", "is_staff", "is_active", "phone_number", "user_type")
    list_filter = (
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
    )
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("email", "password", "user_type")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone_number", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )


