from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.users.services import activate_user, deactivate_user

User = get_user_model()


class UserServicesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="worker1",
            email="worker1@example.com",
            password="StrongPass123!",
            is_active=True,
        )

    def test_deactivate_user(self):
        deactivate_user(self.user)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activate_user(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        activate_user(self.user)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)