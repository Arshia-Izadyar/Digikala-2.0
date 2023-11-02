from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Address


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("email","username", "is_staff", "is_active", "phone_number", "user_type")
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
        (None, {"fields": ("email", "password", "user_type", "birth_date", "phone_number", "firstname", "lastname")}),
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



@admin.register(Address)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "zip_code", "city")
    fields = ("user", "address", "zip_code", "city", "phone_number", "receiver_name")