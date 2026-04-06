from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthFlowIntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="authuser",
            email="authuser@example.com",
            password="StrongPass123!",
        )

    def test_root_redirects_to_login_when_anonymous(self):
        response = self.client.get(reverse("root"))
        self.assertRedirects(response, reverse("login"))

    def test_root_redirects_to_dashboard_when_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("root"))
        self.assertRedirects(response, reverse("dashboard_home"))

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Iniciar sesión")