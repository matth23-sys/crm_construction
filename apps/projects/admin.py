from django.contrib import admin

from .models import Project, ProjectAssignment, ProjectNote


class ProjectAssignmentInline(admin.TabularInline):
    model = ProjectAssignment
    extra = 0
    autocomplete_fields = ("user",)
    fields = ("user", "role", "is_active", "notes", "assigned_at", "unassigned_at")
    readonly_fields = ("assigned_at",)


class ProjectNoteInline(admin.TabularInline):
    model = ProjectNote
    extra = 0
    autocomplete_fields = ("author",)
    fields = ("author", "note_type", "body", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "client",
        "status",
        "responsible",
        "start_date",
        "expected_end_date",
        "updated_at",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = (
        "name",
        "description",
        "location",
        "client__legal_name",
        "client__commercial_name",
    )
    autocomplete_fields = ("client", "opportunity", "responsible")
    inlines = (ProjectAssignmentInline, ProjectNoteInline)


@admin.register(ProjectAssignment)
class ProjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "role", "is_active", "assigned_at", "unassigned_at")
    list_filter = ("role", "is_active", "assigned_at")
    search_fields = ("project__name", "user__username", "user__email")
    autocomplete_fields = ("project", "user")


@admin.register(ProjectNote)
class ProjectNoteAdmin(admin.ModelAdmin):
    list_display = ("project", "author", "note_type", "created_at")
    list_filter = ("note_type", "created_at")
    search_fields = ("project__name", "body", "author__username", "author__email")
    autocomplete_fields = ("project", "author")