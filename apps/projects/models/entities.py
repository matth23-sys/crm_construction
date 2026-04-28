from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from core.db.base import BaseModel
from apps.clients.models import Client
from apps.sales.models import Opportunity

from .choices import (
    ProjectAssignmentRole,
    ProjectNoteType,
    ProjectStatus,
)


class Project(BaseModel):
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="projects",
    )
    opportunity = models.OneToOneField(
        Opportunity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="project",
    )
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects_as_responsible",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.PENDING,
    )
    contract_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    start_date = models.DateField(null=True, blank=True)
    expected_end_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        permissions = (
            ("manage_assignments", "Can manage project assignments"),
            ("add_project_note", "Can add project note"),
            ("create_project_from_opportunity", "Can create project from opportunity"),
        )

    def __str__(self) -> str:
        return f"{self.name} - {self.client}"

    def clean(self) -> None:
        errors = {}

        if self.opportunity_id and self.client_id and self.opportunity.client_id != self.client_id:
            errors["opportunity"] = "Selected opportunity does not belong to the selected client."

        if self.start_date and self.expected_end_date and self.expected_end_date < self.start_date:
            errors["expected_end_date"] = "Expected end date cannot be earlier than start date."

        if self.start_date and self.actual_end_date and self.actual_end_date < self.start_date:
            errors["actual_end_date"] = "Actual end date cannot be earlier than start date."

        if errors:
            raise ValidationError(errors)


class ProjectAssignment(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_assignments",
    )
    role = models.CharField(
        max_length=20,
        choices=ProjectAssignmentRole.choices,
        default=ProjectAssignmentRole.WORKER,
    )
    notes = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    unassigned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-is_active", "role", "user__username")
        constraints = [
            models.UniqueConstraint(
                fields=("project", "user"),
                condition=Q(is_active=True),
                name="unique_active_project_assignment_per_user",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.project} ({self.get_role_display()})"

    def clean(self) -> None:
        errors = {}

        if self.unassigned_at and self.is_active:
            errors["unassigned_at"] = "Inactive assignments only can have unassigned_at set."

        if errors:
            raise ValidationError(errors)


class ProjectNote(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="project_notes",
    )
    note_type = models.CharField(
        max_length=20,
        choices=ProjectNoteType.choices,
        default=ProjectNoteType.INTERNAL,
    )
    body = models.TextField()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.project} - {self.get_note_type_display()}"