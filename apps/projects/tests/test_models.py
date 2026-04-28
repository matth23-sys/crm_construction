from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase

from apps.clients.models import Client
from apps.projects.models import Project, ProjectAssignment
from apps.projects.models.choices import ProjectAssignmentRole

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
        "legal_name": "ACME Construction LLC",
        "commercial_name": "ACME",
        "document_number": "1234567890",
        "email": "acme@example.com",
        "phone": "0999999999",
        "alternate_phone": "0888888888",
        "address": "Main Street 123",
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


class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="lead_user",
            email="lead@example.com",
            password="StrongPass123!",
        )
        self.client_obj = Client.objects.create(**_build_client_payload())

    def test_project_string_representation(self):
        project = Project.objects.create(
            client=self.client_obj,
            responsible=self.user,
            name="Kitchen remodel",
        )
        self.assertIn("Kitchen remodel", str(project))

    def test_assignment_clean_rejects_active_with_unassigned_at(self):
        project = Project.objects.create(
            client=self.client_obj,
            responsible=self.user,
            name="Bathroom remodel",
        )

        assignment = ProjectAssignment(
            project=project,
            user=self.user,
            role=ProjectAssignmentRole.RESPONSIBLE,
            is_active=True,
        )
        assignment.unassigned_at = project.created_at

        with self.assertRaises(ValidationError):
            assignment.full_clean()