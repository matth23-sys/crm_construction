from django.db.models import Count, Prefetch, Q

from .models import Project, ProjectAssignment, ProjectNote


def get_project_base_queryset():
    return (
        Project.objects.select_related("client", "opportunity", "responsible")
        .annotate(
            active_assignments_count=Count(
                "assignments",
                filter=Q(assignments__is_active=True),
                distinct=True,
            ),
            notes_count=Count("notes", distinct=True),
        )
    )


def get_project_list(*, filters=None):
    filters = filters or {}
    queryset = get_project_base_queryset()

    q = (filters.get("q") or "").strip()
    status = filters.get("status")
    client = filters.get("client")
    responsible = filters.get("responsible")

    if q:
        queryset = queryset.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(location__icontains=q)
            | Q(client__legal_name__icontains=q)
            | Q(client__commercial_name__icontains=q)
            | Q(client__document_number__icontains=q)
        ).distinct()

    if status:
        queryset = queryset.filter(status=status)

    if client:
        queryset = queryset.filter(client=client)

    if responsible:
        queryset = queryset.filter(responsible=responsible)

    return queryset


def get_project_detail(*, pk):
    active_assignments = ProjectAssignment.objects.select_related("user").filter(
        is_active=True
    ).order_by("role", "user__username")

    ordered_notes = ProjectNote.objects.select_related("author").order_by("-created_at")

    return (
        Project.objects.select_related("client", "opportunity", "responsible")
        .prefetch_related(
            Prefetch(
                "assignments",
                queryset=active_assignments,
                to_attr="prefetched_active_assignments",
            ),
            Prefetch(
                "notes",
                queryset=ordered_notes,
                to_attr="prefetched_notes",
            ),
        )
        .get(pk=pk)
    )


def get_projects_for_user(*, user):
    return (
        get_project_base_queryset()
        .filter(
            Q(responsible=user)
            | Q(assignments__user=user, assignments__is_active=True)
        )
        .distinct()
    )