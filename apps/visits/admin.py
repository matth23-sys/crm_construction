from django.contrib import admin
from .models import TechnicalVisit, VisitReminderLog

@admin.register(TechnicalVisit)
class TechnicalVisitAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "project",
        "responsible",
        "scheduled_for",
        "status",
        "reminder_enabled",
    )
    list_filter = ("status", "reminder_enabled", "scheduled_for")
    search_fields = (
        "title",
        "client__legal_name",
        "client__commercial_name",
        "project__name",
        "responsible__username",
        "location",
    )
    autocomplete_fields = ("client", "project", "responsible", "created_by", "updated_by")

@admin.register(VisitReminderLog)
class VisitReminderLogAdmin(admin.ModelAdmin):
    list_display = (
        "visit",
        "recipient_email",
        "reminder_type",
        "status",
        "sent_at",
        "created_at",
    )
    list_filter = ("status", "reminder_type", "created_at")
    search_fields = ("visit__title", "recipient_email", "error_message")
    autocomplete_fields = ("visit",)
    readonly_fields = ("created_at", "updated_at")