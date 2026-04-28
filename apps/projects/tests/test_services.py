from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase

from apps.clients.models import Client
from apps.projects.models import ProjectAssignment, ProjectNote
from apps.projects.models.choices import ProjectAssignmentRole, ProjectNoteType
from apps.projects.services import (
    add_project_note,
    assign_user_to_project,
    create_project,
    update_project,
)

User = get_user_model()


def _choice_value(model_class, field_name, fallback=""):
    try:
        field = model_class._meta.get_field(field_name)
    except Exception:
        return fallback

    default = getattr(field, "default", models.NOT_PROVIDED)
    if default is not models.NOT_PROVIDED:
        return default() if callable(default) else default

    if getattr(field, "choices", None):
        return field.choices[0][0]

    return fallback


def _build_client_payload():
    payload = {
        "legal_name": "North Build LLC",
        "commercial_name": "North Build",
        "document_number": "1799999999001",
        "email": "north@example.com",
        "phone": "0999999999",
        "alternate_phone": "0888888888",
        "address": "Central Avenue",
        "city": "Quito",
        "state": "Pichincha",
        "country": "EC",
        "notes": "",
        "client_type": _choice_value(Client, "client_type"),
        "status": _choice_value(Client, "status"),
        "is_active": True,
    }
    concrete_fields = {
        field.name
        for field in Client._meta.get_fields()
        if getattr(field, "concrete", False) and not field.auto_created
    }
    return {key: value for key, value in payload.items() if key in concrete_fields}


class ProjectServiceTests(TestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username="manager",
            email="manager@example.com",
            password="StrongPass123!",
        )
        self.worker = User.objects.create_user(
            username="worker",
            email="worker@example.com",
            password="StrongPass123!",
        )
        self.client_obj = Client.objects.create(**_build_client_payload())

    def test_create_project_creates_primary_responsible_assignment(self):
        project = create_project(
            data={
                "client": self.client_obj,
                "responsible": self.manager,
                "name": "Roof replacement",
            },
            created_by=self.manager,
        )

        self.assertEqual(project.responsible, self.manager)
        self.assertTrue(
            ProjectAssignment.objects.filter(
                project=project,
                user=self.manager,
                role=ProjectAssignmentRole.RESPONSIBLE,
                is_active=True,
            ).exists()
        )

    def test_assign_user_to_project_reuses_existing_active_assignment(self):
        project = create_project(
            data={
                "client": self.client_obj,
                "responsible": self.manager,
                "name": "Deck repair",
            },
            created_by=self.manager,
        )

        first_assignment = assign_user_to_project(
            project=project,
            user=self.worker,
            role=ProjectAssignmentRole.WORKER,
            assigned_by=self.manager,
            notes="Initial assignment",
        )

        second_assignment = assign_user_to_project(
            project=project,
            user=self.worker,
            role=ProjectAssignmentRole.SUPERVISOR,
            assigned_by=self.manager,
            notes="Promoted",
        )

        self.assertEqual(first_assignment.pk, second_assignment.pk)
        self.assertEqual(second_assignment.role, ProjectAssignmentRole.SUPERVISOR)

    def test_update_project_changes_primary_responsible_assignment(self):
        other_manager = User.objects.create_user(
            username="other_manager",
            email="other_manager@example.com",
            password="StrongPass123!",
        )

        project = create_project(
            data={
                "client": self.client_obj,
                "responsible": self.manager,
                "name": "Flooring project",
            },
            created_by=self.manager,
        )

        update_project(
            project,
            data={
                "client": self.client_obj,
                "responsible": other_manager,
                "name": "Flooring project",
            },
            updated_by=self.manager,
        )

        self.assertTrue(
            ProjectAssignment.objects.filter(
                project=project,
                user=other_manager,
                role=ProjectAssignmentRole.RESPONSIBLE,
                is_active=True,
            ).exists()
        )

    def test_add_project_note(self):
        project = create_project(
            data={
                "client": self.client_obj,
                "responsible": self.manager,
                "name": "Interior painting",
            },
            created_by=self.manager,
        )

        note = add_project_note(
            project=project,
            author=self.manager,
            body="Client approved final scope.",
            note_type=ProjectNoteType.INTERNAL,
        )

        self.assertEqual(note.project, project)
        self.assertEqual(note.author, self.manager)
        self.assertTrue(ProjectNote.objects.filter(pk=note.pk).exists())