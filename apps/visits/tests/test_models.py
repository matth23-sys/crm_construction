from decimal import Decimal
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.clients.models import Client
from apps.projects.models import Project
from apps.visits.models import TechnicalVisit


class TechnicalVisitModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="visitmodel",
            email="visitmodel@example.com",
            password="StrongPass123!",
        )

        cls.client_obj = Client.objects.create(
            legal_name="Visit Client",
            commercial_name="Visit Client",
            client_type="company",
            status="active",
            email="visit-client@example.com",
            phone="0999999999",
            created_by=cls.user,
            updated_by=cls.user,
        )

        cls.project = Project.objects.create(
            client=cls.client_obj,
            responsible=cls.user,
            name="Visit Project",
            description="Project for visit tests",
            location="Quito",
            status="pending",
            contract_amount=Decimal("0.00"),
            created_by=cls.user,
            updated_by=cls.user,
        )

    def test_visit_end_must_be_after_start(self):
        start = timezone.now() + timedelta(days=1)
        visit = TechnicalVisit(
            client=self.client_obj,
            project=self.project,
            responsible=self.user,
            title="Invalid visit",
            scheduled_start=start,
            scheduled_end=start,
        )

        with self.assertRaises(ValidationError):
            visit.full_clean()