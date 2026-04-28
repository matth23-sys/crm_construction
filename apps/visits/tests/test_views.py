from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.clients.models import Client
from apps.projects.models import Project
from apps.visits.models import TechnicalVisit


class TechnicalVisitViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="visitview",
            email="visitview@example.com",
            password="StrongPass123!",
        )

        cls.client_obj = Client.objects.create(
            legal_name="View Visit Client",
            commercial_name="View Visit Client",
            client_type="company",
            status="active",
            email="viewvisit-client@example.com",
            phone="0777777777",
            created_by=cls.user,
            updated_by=cls.user,
        )

        cls.project = Project.objects.create(
            client=cls.client_obj,
            responsible=cls.user,
            name="View Visit Project",
            description="Visit project view tests",
            location="Cuenca",
            status="pending",
            contract_amount=Decimal("0.00"),
            created_by=cls.user,
            updated_by=cls.user,
        )

    def test_list_requires_permission(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("visits:list"))
        self.assertEqual(response.status_code, 403)

    def test_create_visit_view_works_with_permission(self):
        permission = Permission.objects.get(codename="add_technicalvisit")
        self.user.user_permissions.add(permission)

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("visits:create"),
            data={
                "client": str(self.client_obj.pk),
                "project": str(self.project.pk),
                "responsible": str(self.user.pk),
                "title": "On-site review",
                "description": "Technical assessment",
                "location": "Main site",
                "contact_name": "Carlos",
                "contact_email": "carlos@example.com",
                "contact_phone": "12345",
                "scheduled_start": (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M"),
                "scheduled_end": (timezone.now() + timedelta(days=3, hours=1)).strftime("%Y-%m-%dT%H:%M"),
                "status": "scheduled",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(TechnicalVisit.objects.count(), 1)