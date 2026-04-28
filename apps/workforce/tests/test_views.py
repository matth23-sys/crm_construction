from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from apps.clients.models.entities import Client
from apps.projects.models.entities import Project, ProjectAssignment, ProjectNote


class WorkforceViewTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()

        self.worker = self.user_model.objects.create_user(
            username="worker1",
            email="worker1@example.com",
            password="StrongPass123!",
        )
        self.other_worker = self.user_model.objects.create_user(
            username="worker2",
            email="worker2@example.com",
            password="StrongPass123!",
        )
        self.unassigned_user = self.user_model.objects.create_user(
            username="viewer1",
            email="viewer1@example.com",
            password="StrongPass123!",
        )

        workforce_permissions = Permission.objects.filter(
            codename__in=[
                "view_assigned_projects",
                "submit_field_note",
                "update_project_milestone",
            ]
        )

        self.worker.user_permissions.add(*workforce_permissions)
        self.other_worker.user_permissions.add(*workforce_permissions)
        self.unassigned_user.user_permissions.add(*workforce_permissions)

        self.client_obj = Client.objects.create(
            legal_name="Client Test",
            commercial_name="Client Test",
            client_type="individual",
            email="client@example.com",
            phone="0999999999",
            status="active",
            is_active=True,
        )

        self.project = Project.objects.create(
            client=self.client_obj,
            name="Assigned Project",
            location="Jobsite A",
            description="Assigned worker project",
            status="pending",
            responsible=self.worker,
            created_by=self.worker,
            updated_by=self.worker,
        )

        self.other_project = Project.objects.create(
            client=self.client_obj,
            name="Other Project",
            location="Jobsite B",
            description="Other worker project",
            status="pending",
            responsible=self.other_worker,
            created_by=self.other_worker,
            updated_by=self.other_worker,
        )

        ProjectAssignment.objects.create(
            project=self.project,
            user=self.worker,
            role="worker",
            is_active=True,
        )
        ProjectAssignment.objects.create(
            project=self.other_project,
            user=self.other_worker,
            role="worker",
            is_active=True,
        )

    def test_worker_list_shows_only_assigned_projects(self):
        self.client.force_login(self.worker)
        response = self.client.get(reverse("workforce:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Assigned Project")
        self.assertNotContains(response, "Other Project")

    def test_unassigned_user_cannot_access_project_detail(self):
        self.client.force_login(self.unassigned_user)
        response = self.client.get(
            reverse("workforce:detail", kwargs={"pk": self.project.pk})
        )

        self.assertEqual(response.status_code, 403)

    def test_worker_can_create_field_note(self):
        self.client.force_login(self.worker)
        response = self.client.post(
            reverse("workforce:note_create", kwargs={"pk": self.project.pk}),
            data={"body": "Finished excavation in area 2."},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ProjectNote.objects.filter(
                project=self.project,
                note_type="field_update",
                body="Finished excavation in area 2.",
            ).exists()
        )

    def test_worker_can_update_allowed_milestone(self):
        self.client.force_login(self.worker)
        response = self.client.post(
            reverse("workforce:milestone_update", kwargs={"pk": self.project.pk}),
            data={"action": "start_work"},
        )

        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, "in_progress")