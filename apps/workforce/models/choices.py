from django.db import models


class WorkforceMilestoneAction(models.TextChoices):
    START_WORK = "start_work", "Start work"
    COMPLETE_WORK = "complete_work", "Mark as completed"


WORKFORCE_ACTION_CONFIG = {
    WorkforceMilestoneAction.START_WORK: {
        "from_statuses": {"pending"},
        "to_status": "in_progress",
        "label": WorkforceMilestoneAction.START_WORK.label,
    },
    WorkforceMilestoneAction.COMPLETE_WORK: {
        "from_statuses": {"in_progress"},
        "to_status": "completed",
        "label": WorkforceMilestoneAction.COMPLETE_WORK.label,
    },
}


def get_available_actions_for_status(current_status: str):
    return [
        action
        for action, config in WORKFORCE_ACTION_CONFIG.items()
        if current_status in config["from_statuses"]
    ]