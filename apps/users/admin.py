from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, UserAccessLog


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "job_title",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("username", "email", "first_name", "last_name", "job_title")
    ordering = ("username",)
    filter_horizontal = ("groups", "user_permissions")

    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Información CRM",
            {
                "fields": (
                    "phone",
                    "job_title",
                    "must_change_password",
                )
            },
        ),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            "Información CRM",
            {
                "fields": (
                    "email",
                    "phone",
                    "job_title",
                    "must_change_password",
                )
            },
        ),
    )


@admin.register(UserAccessLog)
class UserAccessLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "user",
        "identifier",
        "event_type",
        "status",
        "ip_address",
        "request_id",
    )
    list_filter = ("event_type", "status", "created_at")
    search_fields = ("identifier", "detail", "ip_address", "request_id", "user__username")
    readonly_fields = (
        "user",
        "identifier",
        "event_type",
        "status",
        "ip_address",
        "user_agent",
        "request_id",
        "detail",
        "metadata",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False