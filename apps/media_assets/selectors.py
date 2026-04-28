from django.db.models import Case, IntegerField, Q, Value, When, Count

from apps.projects.models import Project

from .models import PhotoClassification, ProjectPhoto


def get_project_gallery_project(project_id):
    return Project.objects.select_related("client", "responsible").get(pk=project_id)


def get_project_photo_base_queryset():
    return ProjectPhoto.objects.select_related(
        "project",
        "project__client",
        "created_by",
        "updated_by",
    )


def get_project_gallery(project, filters=None):
    filters = filters or {}
    queryset = get_project_photo_base_queryset().filter(project=project)

    query = (filters.get("q") or "").strip()
    classification = filters.get("classification") or ""

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(original_filename__icontains=query)
        )

    if classification:
        queryset = queryset.filter(classification=classification)

    return queryset.annotate(
        classification_order=Case(
            When(classification=PhotoClassification.BEFORE, then=Value(1)),
            When(classification=PhotoClassification.IN_PROGRESS, then=Value(2)),
            When(classification=PhotoClassification.FINAL, then=Value(3)),
            default=Value(99),
            output_field=IntegerField(),
        )
    ).order_by("classification_order", "-taken_at", "-created_at")


def get_project_gallery_counts(project):
    raw = (
        get_project_photo_base_queryset()
        .filter(project=project)
        .values("classification")
        .annotate(total=Count("id"))
    )
    indexed = {row["classification"]: row["total"] for row in raw}

    return {
        PhotoClassification.BEFORE: indexed.get(PhotoClassification.BEFORE, 0),
        PhotoClassification.IN_PROGRESS: indexed.get(PhotoClassification.IN_PROGRESS, 0),
        PhotoClassification.FINAL: indexed.get(PhotoClassification.FINAL, 0),
    }


def get_project_photo_detail(photo_id):
    return get_project_photo_base_queryset().get(pk=photo_id)