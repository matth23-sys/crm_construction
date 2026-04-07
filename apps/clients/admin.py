from django.contrib import admin

from .models import Client, ClientInteraction


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "client_type",
        "document_number",
        "email",
        "phone",
        "status",
        "is_active",
        "created_at",
    )
    list_filter = ("status", "client_type", "is_active", "country", "city")
    search_fields = (
        "legal_name",
        "commercial_name",
        "document_number",
        "email",
        "phone",
        "alternate_phone",
    )
    readonly_fields = ("created_at", "updated_at", "deactivated_at")
    autocomplete_fields = ("deactivated_by",)
    ordering = ("legal_name", "commercial_name")

    fieldsets = (
        (
            "Información principal",
            {
                "fields": (
                    "legal_name",
                    "commercial_name",
                    "client_type",
                    "document_number",
                    "email",
                    "phone",
                    "alternate_phone",
                )
            },
        ),
        (
            "Ubicación",
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "country",
                )
            },
        ),
        (
            "Estado y control",
            {
                "fields": (
                    "status",
                    "is_active",
                    "deactivated_at",
                    "deactivated_by",
                )
            },
        ),
        (
            "Notas",
            {
                "fields": ("notes",)
            },
        ),
        (
            "Auditoría",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Cliente")
    def client_name(self, obj):
        return obj.display_name


@admin.register(ClientInteraction)
class ClientInteractionAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "interaction_type",
        "summary",
        "occurred_at",
        "follow_up_at",
        "registered_by",
        "created_at",
    )
    list_filter = ("interaction_type", "occurred_at", "follow_up_at")
    search_fields = (
        "client__legal_name",
        "client__commercial_name",
        "summary",
        "description",
    )
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("client", "registered_by")
    ordering = ("-occurred_at", "-created_at")