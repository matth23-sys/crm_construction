from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.clients.models import Client
from apps.clients.models.choices import ClientStatus, ClientType, InteractionType
from apps.clients.services import (
    create_client,
    deactivate_client,
    reactivate_client,
    register_client_interaction,
    update_client,
)


User = get_user_model()


class ClientServicesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="manager",
            email="manager@example.com",
            password="StrongPass123!",
        )

    def test_create_client_normalizes_email(self):
        client = create_client(
            data={
                "legal_name": "Cliente Demo",
                "commercial_name": "Demo",
                "client_type": ClientType.COMPANY,
                "document_number": "0999999999",
                "email": "CLIENTE@EXAMPLE.COM ",
                "phone": "0991111111",
                "alternate_phone": "",
                "address": "",
                "city": "",
                "state": "",
                "country": "Ecuador",
                "notes": "",
            },
            user=self.user,
        )

        self.assertEqual(client.email, "cliente@example.com")

    def test_update_client_changes_basic_data(self):
        client = Client.objects.create(
            legal_name="Cliente Inicial",
            client_type=ClientType.COMPANY,
        )

        updated = update_client(
            client=client,
            data={
                "legal_name": "Cliente Editado",
                "commercial_name": "Marca Editada",
                "client_type": ClientType.COMPANY,
                "document_number": "1234567890",
                "email": "editado@example.com",
                "phone": "0999999999",
                "alternate_phone": "",
                "address": "Dirección",
                "city": "Quito",
                "state": "Pichincha",
                "country": "Ecuador",
                "notes": "Notas internas",
            },
            user=self.user,
        )

        self.assertEqual(updated.legal_name, "Cliente Editado")
        self.assertEqual(updated.city, "Quito")

    def test_deactivate_and_reactivate_client(self):
        client = Client.objects.create(
            legal_name="Cliente Activo",
            client_type=ClientType.COMPANY,
        )

        deactivate_client(client=client, user=self.user)
        client.refresh_from_db()
        self.assertEqual(client.status, ClientStatus.INACTIVE)
        self.assertFalse(client.is_active)

        reactivate_client(client=client, user=self.user)
        client.refresh_from_db()
        self.assertEqual(client.status, ClientStatus.ACTIVE)
        self.assertTrue(client.is_active)

    def test_register_client_interaction_assigns_user(self):
        client = Client.objects.create(
            legal_name="Cliente con historial",
            client_type=ClientType.COMPANY,
        )

        interaction = register_client_interaction(
            client=client,
            data={
                "interaction_type": InteractionType.MEETING,
                "summary": "Reunión inicial",
                "description": "Se revisó alcance del proyecto.",
                "occurred_at": "2026-04-06T10:00",
                "follow_up_at": None,
            },
            user=self.user,
        )

        self.assertEqual(interaction.client, client)
        self.assertEqual(interaction.registered_by, self.user)