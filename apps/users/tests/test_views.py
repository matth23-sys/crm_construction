from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="profileuser",
            email="profile@example.com",
            password="StrongPass123!",
        )

    def test_profile_requires_login(self):
        response = self.client.get(reverse("user_profile"))
        self.assertEqual(response.status_code, 302)

    def test_profile_view_loads_when_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("user_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mi perfil")

    def test_profile_can_be_updated(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("user_profile"),
            {
                "first_name": "Mateo",
                "last_name": "Guerron",
                "email": "new@example.com",
                "phone": "+593999999999",
                "job_title": "Manager",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Mateo")
        self.assertEqual(self.user.email, "new@example.com")