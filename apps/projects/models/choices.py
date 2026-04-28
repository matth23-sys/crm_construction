from django.db import models


class ProjectStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"


class ProjectAssignmentRole(models.TextChoices):
    RESPONSIBLE = "responsible", "Responsible"
    SUPERVISOR = "supervisor", "Supervisor"
    WORKER = "worker", "Worker"
    SUPPORT = "support", "Support"


class ProjectNoteType(models.TextChoices):
    INTERNAL = "internal", "Internal"
    FIELD_UPDATE = "field_update", "Field Update"