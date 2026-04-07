from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.clients.models import Client, ClientInteraction
from apps.clients.models.choices import ClientStatus, ClientType, InteractionType


User = get_user_model()


class ClientModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="StrongPass123!",
        )

    def test_display_name_prefers_commercial_name(self):
        client = Client.objects.create(
            legal_name="Constructora XYZ S.A.",
            commercial_name="XYZ Constructora",
            client_type=ClientType.COMPANY,
        )
        self.assertEqual(client.display_name, "XYZ Constructora")

    def test_deactivate_updates_status(self):
        client = Client.objects.create(
            legal_name="Cliente Demo",
            client_type=ClientType.COMPANY,
        )

        client.deactivate(user=self.user)
        client.save()

        self.assertFalse(client.is_active)
        self.assertEqual(client.status, ClientStatus.INACTIVE)
        self.assertIsNotNone(client.deactivated_at)
        self.assertEqual(client.deactivated_by, self.user)


class ClientInteractionModelTests(TestCase):
    def test_string_representation(self):
        client = Client.objects.create(
            legal_name="Cliente Uno",
            client_type=ClientType.COMPANY,
        )
        interaction = ClientInteraction.objects.create(
            client=client,
            interaction_type=InteractionType.CALL,
            summary="Primera llamada",
        )
        self.assertIn("Cliente Uno", str(interaction))