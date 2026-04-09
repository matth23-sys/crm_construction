from django.contrib import admin

from .models import Opportunity, OpportunityStage, OpportunityStageHistory


class OpportunityStageHistoryInline(admin.TabularInline):
    model = OpportunityStageHistory
    extra = 0
    can_delete = False
    fields = ("from_stage", "to_stage", "changed_by", "moved_at", "note")
    readonly_fields = ("from_stage", "to_stage", "changed_by", "moved_at", "note")
    ordering = ("-moved_at", "-created_at")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(OpportunityStage)
class OpportunityStageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "position",
        "is_active",
        "is_default",
        "is_won_stage",
        "is_lost_stage",
    )
    list_filter = ("is_active", "is_default", "is_won_stage", "is_lost_stage")
    search_fields = ("name", "code", "description")
    ordering = ("position", "name")


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client_display_name",
        "stage",
        "status",
        "responsible",
        "estimated_value",
        "expected_close_date",
        "closed_at",
    )
    list_filter = ("status", "stage", "source", "responsible")
    search_fields = (
        "title",
        "description",
        "client__legal_name",
        "client__commercial_name",
        "client__document_number",
        "client__email",
    )
    autocomplete_fields = ("client", "stage", "responsible")
    readonly_fields = (
        "status",
        "closed_at",
        "converted_to_project_at",
        "created_at",
        "updated_at",
    )
    inlines = (OpportunityStageHistoryInline,)

    fieldsets = (
        (
            "Commercial data",
            {
                "fields": (
                    "client",
                    "title",
                    "description",
                    "stage",
                    "status",
                    "responsible",
                    "estimated_value",
                    "expected_close_date",
                    "source",
                )
            },
        ),
        (
            "Operational notes",
            {
                "fields": (
                    "internal_notes",
                    "loss_reason",
                )
            },
        ),
        (
            "Lifecycle",
            {
                "fields": (
                    "closed_at",
                    "converted_to_project_at",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Client")
    def client_display_name(self, obj):
        return getattr(obj.client, "display_name", None) or getattr(obj.client, "commercial_name", None) or obj.client.legal_name


@admin.register(OpportunityStageHistory)
class OpportunityStageHistoryAdmin(admin.ModelAdmin):
    list_display = ("opportunity", "from_stage", "to_stage", "changed_by", "moved_at")
    list_filter = ("to_stage", "from_stage", "moved_at")
    search_fields = ("opportunity__title", "note", "changed_by__username", "changed_by__email")
    autocomplete_fields = ("opportunity", "from_stage", "to_stage", "changed_by")
    readonly_fields = (
        "opportunity",
        "from_stage",
        "to_stage",
        "changed_by",
        "note",
        "moved_at",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False