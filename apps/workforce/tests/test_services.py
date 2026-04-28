from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.clients.models.entities import Client
from apps.projects.models.entities import Project, ProjectAssignment, ProjectNote
from apps.workforce.models.choices import WorkforceMilestoneAction
from apps.workforce.services import apply_worker_milestone_action, create_field_note


class WorkforceServiceTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.worker = self.user_model.objects.create_user(
            username="worker1",
            email="worker1@example.com",
            password="StrongPass123!",
        )

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
            name="Field Project",
            location="On site",
            description="Operational project",
            status="pending",
            responsible=self.worker,
            created_by=self.worker,
            updated_by=self.worker,
        )

        ProjectAssignment.objects.create(
            project=self.project,
            user=self.worker,
            role="worker",
            is_active=True,
        )

    def test_create_field_note(self):
        note = create_field_note(
            project=self.project,
            author=self.worker,
            body="Concrete poured in sector A.",
        )

        self.assertEqual(note.project, self.project)
        self.assertEqual(note.author, self.worker)
        self.assertEqual(note.note_type, "field_update")
        self.assertEqual(note.body, "Concrete poured in sector A.")

    def test_apply_worker_milestone_action_updates_status_and_creates_note(self):
        apply_worker_milestone_action(
            project=self.project,
            user=self.worker,
            action=WorkforceMilestoneAction.START_WORK,
        )

        self.project.refresh_from_db()
        self.assertEqual(self.project.status, "in_progress")
        self.assertTrue(
            ProjectNote.objects.filter(
                project=self.project,
                note_type="field_update",
            ).exists()
        )