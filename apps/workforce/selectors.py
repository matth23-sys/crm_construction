from django.db.models import Q, Subquery

from apps.projects.models.entities import Project, ProjectAssignment, ProjectNote


ACTIVE_WORKFORCE_ASSIGNMENT_ROLES = (
    "worker",
    "support",
    "supervisor",
    "responsible",
)


def get_assigned_project_ids_for_user(*, user):
    return ProjectAssignment.objects.filter(
        user=user,
        is_active=True,
        role__in=ACTIVE_WORKFORCE_ASSIGNMENT_ROLES,
    ).values("project_id")


def get_my_assigned_projects(*, user, filters=None):
    queryset = Project.objects.select_related(
        "client",
        "opportunity",
        "responsible",
    ).filter(
        id__in=Subquery(get_assigned_project_ids_for_user(user=user))
    ).distinct().order_by("-updated_at", "-created_at")

    if not filters:
        return queryset

    search = (filters.get("search") or "").strip()
    status = (filters.get("status") or "").strip()

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(location__icontains=search)
            | Q(client__legal_name__icontains=search)
            | Q(client__commercial_name__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    return queryset


def get_assigned_project_for_user(*, user, project_id):
    return Project.objects.select_related(
        "client",
        "opportunity",
        "responsible",
    ).filter(
        id=project_id,
        id__in=Subquery(get_assigned_project_ids_for_user(user=user)),
    ).first()


def get_assigned_project_detail(*, user, project_id):
    project = get_assigned_project_for_user(user=user, project_id=project_id)
    if project is None:
        return None

    active_assignments = ProjectAssignment.objects.select_related("user").filter(
        project=project,
        is_active=True,
    ).order_by("assigned_at", "created_at")

    field_notes = ProjectNote.objects.select_related("author").filter(
        project=project,
        note_type="field_update",
    ).order_by("-created_at")

    return {
        "project": project,
        "active_assignments": active_assignments,
        "field_notes": field_notes,
    }