from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.utils import timezone

from apps.clients.models import Client
from apps.notifications.services import send_visit_reminder_email
from apps.projects.models import Project
from apps.visits.models import TechnicalVisit


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class NotificationServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="notifyuser",
            email="notifyuser@example.com",
            password="StrongPass123!",
        )

        cls.client_obj = Client.objects.create(
            legal_name="Notify Client",
            commercial_name="Notify Client",
            client_type="company",
            status="active",
            email="notify-client@example.com",
            phone="0666666666",
            created_by=cls.user,
            updated_by=cls.user,
        )

        cls.project = Project.objects.create(
            client=cls.client_obj,
            responsible=cls.user,
            name="Notify Project",
            description="Notification project",
            location="Loja",
            status="pending",
            contract_amount=Decimal("0.00"),
            created_by=cls.user,
            updated_by=cls.user,
        )

        cls.visit = TechnicalVisit.objects.create(
            client=cls.client_obj,
            project=cls.project,
            responsible=cls.user,
            title="Notify visit",
            description="Reminder body test",
            location="Office",
            scheduled_start=timezone.now() + timedelta(days=1),
            scheduled_end=timezone.now() + timedelta(days=1, hours=1),
            status="scheduled",
            created_by=cls.user,
            updated_by=cls.user,
        )

    def test_send_visit_reminder_email(self):
        result = send_visit_reminder_email(self.visit, "day_before", run_date=timezone.localdate())

        self.assertEqual(result["recipient_email"], "notifyuser@example.com")
        self.assertEqual(len(mail.outbox), 1)