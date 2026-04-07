from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from apps.users.models import UserAccessLog
from apps.users.models.choices import AccessEventStatus, AccessEventType

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user_successfully(self):
        """Prueba la creación básica de un usuario."""
        user = User.objects.create_user(
            username="mateo",
            email="mateo@example.com",
            password="StrongPass123!",
        )

        self.assertEqual(user.username, "mateo")
        self.assertEqual(user.email, "mateo@example.com")
        self.assertTrue(user.check_password("StrongPass123!"))

    def test_email_must_be_unique(self):
        """Verifica que el email sea único (IntegrityError si se repite)."""
        User.objects.create_user(
            username="user1",
            email="same@example.com",
            password="StrongPass123!",
        )

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="user2",
                email="same@example.com",
                password="StrongPass123!",
            )

    def test_email_is_normalized(self):
        """Comprueba que el email se normalice a minúsculas."""
        user = User.objects.create_user(
            username="mateo",
            email="TEST@EXAMPLE.COM",
            password="StrongPass123!",
        )
        self.assertEqual(user.email, "test@example.com")

    def test_full_name_falls_back_to_username(self):
        """Si no hay nombre completo, se usa el username como fallback."""
        user = User.objects.create_user(
            username="fallbackuser",
            email="fallback@example.com",
            password="StrongPass123!",
        )
        self.assertEqual(user.full_name, "fallbackuser")


class UserAccessLogTests(TestCase):
    def test_access_log_is_created(self):
        """Prueba que se pueda crear un registro de acceso."""
        user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="StrongPass123!",
        )

        log = UserAccessLog.objects.create(
            user=user,
            identifier="admin",
            event_type=AccessEventType.LOGIN,
            status=AccessEventStatus.SUCCESS,
            detail="Inicio correcto",
        )

        self.assertEqual(log.user, user)
        self.assertEqual(log.event_type, AccessEventType.LOGIN)