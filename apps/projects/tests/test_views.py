from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import models
from django.test import TestCase
from django.urls import reverse

from apps.clients.models import Client
from apps.projects.models import Project

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
        "legal_name": "Urban Works LLC",
        "commercial_name": "Urban Works",
        "document_number": "1791111111001",
        "email": "urban@example.com",
        "phone": "0991111111",
        "alternate_phone": "0881111111",
        "address": "North Avenue",
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


def _grant_permissions(user, *codenames):
    permissions = Permission.objects.filter(codename__in=codenames)
    user.user_permissions.add(*permissions)


class ProjectViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="projects_admin",
            email="projects_admin@example.com",
            password="StrongPass123!",
        )
        self.client.force_login(self.user)
        self.client_obj = Client.objects.create(**_build_client_payload())

    def test_project_list_view_with_permission(self):
        _grant_permissions(self.user, "view_project")

        response = self.client.get(reverse("projects:list"))

        self.assertEqual(response.status_code, 200)

    def test_project_create_view(self):
        _grant_permissions(self.user, "add_project", "view_project")

        response = self.client.post(
            reverse("projects:create"),
            data={
                "client": self.client_obj.pk,
                "name": "Kitchen upgrade",
                "status": "pending",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name="Kitchen upgrade").exists())

    def test_project_create_from_opportunity_uses_session_seed(self):
        _grant_permissions(self.user, "add_project", "view_project")

        session = self.client.session
        session["project_seed"] = {
            "client_id": self.client_obj.pk,
            "project_name": "Seeded project",
        }
        session.save()

        response = self.client.post(
            reverse("projects:create_from_opportunity"),
            data={
                "client": self.client_obj.pk,
                "name": "Seeded project",
                "status": "pending",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name="Seeded project").exists())

        session = self.client.session
        self.assertNotIn("project_seed", session)