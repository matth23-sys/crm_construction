from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.utils import timezone

from apps.clients.models import Client
from apps.projects.models import Project
from apps.visits.models import ReminderType, TechnicalVisit, VisitReminderLog
from apps.visits.services import (
    create_technical_visit,
    process_due_visit_reminders,
    update_technical_visit,
)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class TechnicalVisitServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="visitservice",
            email="visitservice@example.com",
            password="StrongPass123!",
        )

        cls.client_obj = Client.objects.create(
            legal_name="Reminder Client",
            commercial_name="Reminder Client",
            client_type="company",
            status="active",
            email="reminder-client@example.com",
            phone="0888888888",
            created_by=cls.user,
            updated_by=cls.user,
        )

        cls.project = Project.objects.create(
            client=cls.client_obj,
            responsible=cls.user,
            name="Reminder Project",
            description="Project reminder",
            location="Guayaquil",
            status="pending",
            contract_amount=Decimal("0.00"),
            created_by=cls.user,
            updated_by=cls.user,
        )

    def test_create_and_reschedule_visit(self):
        visit = create_technical_visit(
            actor=self.user,
            client=self.client_obj,
            project=self.project,
            responsible=self.user,
            title="Initial technical visit",
            description="First review",
            location="Site",
            contact_name="Luis",
            contact_email="luis@example.com",
            contact_phone="123456",
            scheduled_start=timezone.now() + timedelta(days=2),
            scheduled_end=timezone.now() + timedelta(days=2, hours=1),
            status="scheduled",
        )

        new_start = visit.scheduled_start + timedelta(days=1)
        new_end = visit.scheduled_end + timedelta(days=1)

        visit = update_technical_visit(
            visit=visit,
            actor=self.user,
            client=visit.client,
            project=visit.project,
            responsible=visit.responsible,
            title=visit.title,
            description=visit.description,
            location=visit.location,
            contact_name=visit.contact_name,
            contact_email=visit.contact_email,
            contact_phone=visit.contact_phone,
            scheduled_start=new_start,
            scheduled_end=new_end,
            status=visit.status,
        )

        self.assertEqual(visit.reschedule_count, 1)
        self.assertIsNotNone(visit.rescheduled_at)
        self.assertEqual(visit.rescheduled_by, self.user)

    def test_process_due_visit_reminders_sends_once(self):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=1)

        create_technical_visit(
            actor=self.user,
            client=self.client_obj,
            project=self.project,
            responsible=self.user,
            title="Reminder visit",
            description="Check roof",
            location="North site",
            contact_name="Ana",
            contact_email="ana@example.com",
            contact_phone="55555",
            scheduled_start=start,
            scheduled_end=end,
            status="scheduled",
        )

        run_date = timezone.localdate()
        summary_first = process_due_visit_reminders(run_date=run_date)
        summary_second = process_due_visit_reminders(run_date=run_date)

        self.assertEqual(summary_first.get("sent"), 1)
        self.assertEqual(summary_second.get("skipped"), 1)
        self.assertEqual(len(mail.outbox), 1)

        log = VisitReminderLog.objects.get(reminder_type=ReminderType.DAY_BEFORE)
        self.assertEqual(log.status, "sent")