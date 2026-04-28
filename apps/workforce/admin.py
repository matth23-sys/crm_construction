from django.contrib import admin

from .models import WorkforceProject


@admin.register(WorkforceProject)
class WorkforceProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "client", "status", "responsible", "updated_at")
    search_fields = ("name", "client__legal_name", "client__commercial_name")
    list_filter = ("status",)
    autocomplete_fields = ("client", "responsible", "opportunity")