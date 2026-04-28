from django.core.exceptions import ValidationError
from django.db import transaction

from apps.projects.models.entities import ProjectNote

from .models.choices import WORKFORCE_ACTION_CONFIG, WorkforceMilestoneAction


def create_field_note(*, project, author, body: str):
    note = ProjectNote(
        project=project,
        author=author,
        note_type="field_update",
        body=body.strip(),
    )

    if hasattr(note, "created_by_id") and not note.created_by_id:
        note.created_by = author
    if hasattr(note, "updated_by_id"):
        note.updated_by = author

    note.full_clean()
    note.save()
    return note


@transaction.atomic
def apply_worker_milestone_action(*, project, user, action: str):
    try:
        action_enum = WorkforceMilestoneAction(action)
    except ValueError as exc:
        raise ValidationError("Invalid workforce milestone action.") from exc

    config = WORKFORCE_ACTION_CONFIG[action_enum]

    if project.status not in config["from_statuses"]:
        raise ValidationError(
            f"Action '{action_enum.value}' is not allowed from status '{project.status}'."
        )

    project.status = config["to_status"]

    if hasattr(project, "updated_by_id"):
        project.updated_by = user

    project.full_clean()
    project.save()

    create_field_note(
        project=project,
        author=user,
        body=f"Milestone updated: {config['label']}.",
    )

    return project