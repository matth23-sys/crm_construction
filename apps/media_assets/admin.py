from django.contrib import admin

from .models import ProjectPhoto


@admin.register(ProjectPhoto)
class ProjectPhotoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "classification",
        "title",
        "file_size",
        "created_by",
        "created_at",
    )
    list_filter = ("classification", "created_at")
    search_fields = (
        "project__name",
        "project__client__legal_name",
        "title",
        "description",
        "original_filename",
    )
    autocomplete_fields = ("project", "created_by", "updated_by")
    readonly_fields = (
        "original_filename",
        "mime_type",
        "file_size",
        "created_at",
        "updated_at",
    )