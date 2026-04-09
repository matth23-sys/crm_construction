# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, UserAccessLog


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "email",
        "full_name",
        "job_title",
        "is_active",
        "is_staff",
        "must_change_password",
        "created_at",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "must_change_password", "job_title", "groups")
    search_fields = ("username", "email", "first_name", "last_name", "phone")
    ordering = ("-created_at",)
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informacion personal", {"fields": ("first_name", "last_name", "email", "phone", "job_title")}),
        (
            "Permisos y estado",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "must_change_password",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Fechas importantes", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "must_change_password"),
            },
        ),
    )
    
    readonly_fields = ("created_at", "updated_at", "last_login")


@admin.register(UserAccessLog)
class UserAccessLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "event_type",
        "event_status",
        "identifier_used",
        "ip_address",
        "created_at",
    )
    list_filter = ("event_type", "event_status", "created_at")
    search_fields = ("user__email", "user__username", "identifier_used", "ip_address")
    readonly_fields = (
        "user", "event_type", "event_status", "identifier_used",
        "ip_address", "user_agent", "request_id", "details",
        "created_at", "updated_at"
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
