from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.clients.models import Client
from apps.clients.models.choices import ClientType, InteractionType


User = get_user_model()


class ClientViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="adminclient",
            email="adminclient@example.com",
            password="StrongPass123!",
        )
        self.client_record = Client.objects.create(
            legal_name="Cliente Vista",
            client_type=ClientType.COMPANY,
            email="clientevista@example.com",
        )

    def grant_permissions(self, user, *codenames):
        permissions = Permission.objects.filter(codename__in=codenames)
        user.user_permissions.add(*permissions)

    def test_list_requires_login(self):
        response = self.client.get(reverse("clients:list"))
        self.assertEqual(response.status_code, 302)

    def test_user_with_permission_can_access_list(self):
        self.client.login(username="adminclient", password="StrongPass123!")
        self.grant_permissions(self.user, "view_client")

        response = self.client.get(reverse("clients:list"))
        self.assertEqual(response.status_code, 200)

    def test_create_client_view_works(self):
        self.client.login(username="adminclient", password="StrongPass123!")
        self.grant_permissions(
            self.user,
            "add_client",
            "view_client",
            "view_clientinteraction",
        )

        response = self.client.post(
            reverse("clients:create"),
            data={
                "legal_name": "Nuevo Cliente",
                "commercial_name": "NC",
                "client_type": ClientType.COMPANY,
                "document_number": "1234567890",
                "email": "nuevo@example.com",
                "phone": "0990000000",
                "alternate_phone": "",
                "address": "Av. Principal",
                "city": "Quito",
                "state": "Pichincha",
                "country": "Ecuador",
                "notes": "Cliente desde web",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Client.objects.filter(legal_name="Nuevo Cliente").exists())

    def test_detail_without_permission_redirects(self):
        self.client.login(username="adminclient", password="StrongPass123!")

        response = self.client.get(
            reverse("clients:detail", kwargs={"pk": self.client_record.pk})
        )

        self.assertEqual(response.status_code, 302)

    def test_can_register_interaction(self):
        self.client.login(username="adminclient", password="StrongPass123!")
        self.grant_permissions(
            self.user,
            "view_client",
            "view_clientinteraction",
            "add_clientinteraction",
        )

        response = self.client.post(
            reverse("clients:interaction_create", kwargs={"pk": self.client_record.pk}),
            data={
                "interaction_type": InteractionType.CALL,
                "summary": "Llamada de seguimiento",
                "description": "Cliente solicita cotización.",
                "occurred_at": timezone.now().strftime("%Y-%m-%dT%H:%M"),
                "follow_up_at": "",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client_record.interactions.count(), 1)

    def test_can_deactivate_client(self):
        self.client.login(username="adminclient", password="StrongPass123!")
        self.grant_permissions(self.user, "deactivate_client")

        response = self.client.post(
            reverse("clients:deactivate", kwargs={"pk": self.client_record.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.client_record.refresh_from_db()
        self.assertFalse(self.client_record.is_active)