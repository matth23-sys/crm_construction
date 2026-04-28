from copy import deepcopy
from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import Project, ProjectAssignment, ProjectNote
from .models.choices import ProjectAssignmentRole, ProjectNoteType, ProjectStatus


def _apply_user_stamps(instance, *, user, is_create=False):
    if is_create and hasattr(instance, "created_by") and not getattr(instance, "created_by_id", None):
        instance.created_by = user

    if hasattr(instance, "updated_by"):
        instance.updated_by = user


def _apply_project_data(project: Project, *, data: dict):
    payload = deepcopy(data)

    for field in (
        "client",
        "opportunity",
        "responsible",
        "name",
        "description",
        "location",
        "status",
        "contract_amount",
        "start_date",
        "expected_end_date",
        "actual_end_date",
    ):
        if field in payload:
            setattr(project, field, payload[field])

    if project.status == ProjectStatus.COMPLETED and not project.actual_end_date:
        project.actual_end_date = date.today()


@transaction.atomic
def create_project(*, data: dict, created_by):
    project = Project()
    _apply_project_data(project, data=data)
    _apply_user_stamps(project, user=created_by, is_create=True)
    project.full_clean()
    project.save()

    _sync_primary_responsible_assignment(project=project, acting_user=created_by)
    return project


@transaction.atomic
def update_project(project: Project, *, data: dict, updated_by):
    _apply_project_data(project, data=data)
    _apply_user_stamps(project, user=updated_by)
    project.full_clean()
    project.save()

    _sync_primary_responsible_assignment(project=project, acting_user=updated_by)
    return project


@transaction.atomic
def _sync_primary_responsible_assignment(*, project: Project, acting_user):
    # Remove other active RESPONSIBLE assignments if the primary responsible changed.
    active_responsible_assignments = project.assignments.filter(
        is_active=True,
        role=ProjectAssignmentRole.RESPONSIBLE,
    )

    if not project.responsible_id:
        for assignment in active_responsible_assignments:
            assignment.is_active = False
            assignment.unassigned_at = timezone.now()
            _apply_user_stamps(assignment, user=acting_user)
            assignment.full_clean()
            assignment.save(update_fields=["is_active", "unassigned_at", "updated_by", "updated_at"])
        return

    for assignment in active_responsible_assignments.exclude(user=project.responsible):
        assignment.is_active = False
        assignment.unassigned_at = timezone.now()
        _apply_user_stamps(assignment, user=acting_user)
        assignment.full_clean()
        assignment.save(update_fields=["is_active", "unassigned_at", "updated_by", "updated_at"])

    assign_user_to_project(
        project=project,
        user=project.responsible,
        role=ProjectAssignmentRole.RESPONSIBLE,
        assigned_by=acting_user,
        notes="Primary responsible synced from project.",
    )


@transaction.atomic
def assign_user_to_project(*, project: Project, user, role: str, assigned_by, notes: str = ""):
    assignment = project.assignments.filter(user=user, is_active=True).first()

    if assignment:
        assignment.role = role
        assignment.notes = notes
        _apply_user_stamps(assignment, user=assigned_by)
        assignment.full_clean()
        assignment.save()
        return assignment

    assignment = project.assignments.filter(user=user, is_active=False).order_by("-assigned_at").first()
    if assignment:
        assignment.role = role
        assignment.notes = notes
        assignment.is_active = True
        assignment.unassigned_at = None
        _apply_user_stamps(assignment, user=assigned_by)
        assignment.full_clean()
        assignment.save()
        return assignment

    assignment = ProjectAssignment(
        project=project,
        user=user,
        role=role,
        notes=notes,
        is_active=True,
    )
    _apply_user_stamps(assignment, user=assigned_by, is_create=True)
    assignment.full_clean()
    assignment.save()
    return assignment


@transaction.atomic
def deactivate_project_assignment(*, assignment: ProjectAssignment, updated_by):
    if (
        assignment.role == ProjectAssignmentRole.RESPONSIBLE
        and assignment.project.responsible_id == assignment.user_id
    ):
        raise ValidationError(
            "Cannot deactivate the primary responsible assignment without changing the project responsible first."
        )

    assignment.is_active = False
    assignment.unassigned_at = timezone.now()
    _apply_user_stamps(assignment, user=updated_by)
    assignment.full_clean()
    assignment.save()
    return assignment


@transaction.atomic
def add_project_note(*, project: Project, author, body: str, note_type: str = ProjectNoteType.INTERNAL):
    note = ProjectNote(
        project=project,
        author=author,
        body=body,
        note_type=note_type,
    )
    _apply_user_stamps(note, user=author, is_create=True)
    note.full_clean()
    note.save()
    return note