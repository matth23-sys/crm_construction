from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from apps.users.models import UserAccessLog
from apps.users.models.choices import AccessEventType

User = get_user_model()


class ProfileViewTests(TestCase):
    """Pruebas para la vista de perfil propio (primer fragmento)."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="profileuser",
            email="profile@example.com",
            password="StrongPass123!",
        )

    def test_profile_requires_login(self):
        """El perfil redirige a login si no hay autenticación."""
        response = self.client.get(reverse("user_profile"))
        self.assertEqual(response.status_code, 302)

    def test_profile_view_loads_when_authenticated(self):
        """El perfil se carga correctamente para usuario autenticado."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("user_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mi perfil")

    def test_profile_can_be_updated(self):
        """Actualización de datos del perfil."""
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


class UserViewsTests(TestCase):
    """Pruebas para vistas de administración de usuarios (segundo fragmento)."""

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="StrongPass123!",
            is_active=True,
        )
        permissions = Permission.objects.filter(
            content_type__app_label__in=["users", "auth"]
        )
        self.admin.user_permissions.set(permissions)

        self.normal_user = User.objects.create_user(
            username="normal",
            email="normal@example.com",
            password="StrongPass123!",
            is_active=True,
        )

    def test_login_creates_access_log(self):
        """El login exitoso crea un registro en UserAccessLog."""
        response = self.client.post(
            reverse("login"),
            {"username": "admin", "password": "StrongPass123!"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            UserAccessLog.objects.filter(
                identifier="admin",
                event_type=AccessEventType.LOGIN,
            ).exists()
        )

    def test_user_list_requires_permission(self):
        """Usuario sin permiso no puede listar usuarios."""
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse("users:list"))
        self.assertRedirects(response, reverse("users:access_denied"))

    def test_user_list_works_for_privileged_user(self):
        """Usuario con permisos puede listar usuarios."""
        self.client.force_login(self.admin)
        response = self.client.get(reverse("users:list"))
        self.assertEqual(response.status_code, 200)

    def test_user_create_view_creates_user(self):
        """Creación de nuevo usuario por administrador."""
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("users:create"),
            {
                "username": "nuevo",
                "first_name": "Nuevo",
                "last_name": "Usuario",
                "email": "nuevo@example.com",
                "phone": "0988888888",
                "job_title": "Asistente",
                "is_active": True,
                "must_change_password": True,
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="nuevo").exists())

    def test_profile_update_view_updates_self(self):
        """Actualización de perfil propio (vista users:profile)."""
        self.client.force_login(self.normal_user)
        response = self.client.post(
            reverse("users:profile"),
            {
                "first_name": "Normal",
                "last_name": "Actualizado",
                "email": "normal@example.com",
                "phone": "0977777777",
                "job_title": "Operador",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.job_title, "Operador")