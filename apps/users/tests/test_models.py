from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user_successfully(self):
        user = User.objects.create_user(
            username="mateo",
            email="mateo@example.com",
            password="StrongPass123!",
        )

        self.assertEqual(user.username, "mateo")
        self.assertEqual(user.email, "mateo@example.com")
        self.assertTrue(user.check_password("StrongPass123!"))

    def test_email_must_be_unique(self):
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

    def test_full_name_falls_back_to_username(self):
        user = User.objects.create_user(
            username="fallbackuser",
            email="fallback@example.com",
            password="StrongPass123!",
        )

        self.assertEqual(user.full_name, "fallbackuser")