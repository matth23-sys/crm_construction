from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("created_at", "updated_at", "last_login", "date_joined")

    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Información adicional",
            {
                "fields": (
                    "phone",
                    "job_title",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )