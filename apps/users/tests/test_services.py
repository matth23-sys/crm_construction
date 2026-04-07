from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import RequestFactory, TestCase

from apps.users.models import UserAccessLog
from apps.users.models.choices import AccessEventStatus, AccessEventType, DefaultGroup
from apps.users.services import (
    activate_user,
    bootstrap_default_groups,
    create_user,
    deactivate_user,
    register_access_event,
)

User = get_user_model()


class UserServicesTests(TestCase):
    def setUp(self):
        """Configuración común para todos los tests de servicios."""
        self.factory = RequestFactory()
        self.admin = User.objects.create_superuser(
            username="superadmin",
            email="superadmin@example.com",
            password="StrongPass123!",
        )
        self.normal_user = User.objects.create_user(
            username="worker1",
            email="worker1@example.com",
            password="StrongPass123!",
            is_active=True,
        )

    # Tests originales del primer bloque (adaptados a la firma con performed_by)
    def test_deactivate_user(self):
        """Desactivar un usuario (primer bloque, adaptado)."""
        deactivate_user(user=self.normal_user, performed_by=self.admin)
        self.normal_user.refresh_from_db()
        self.assertFalse(self.normal_user.is_active)

    def test_activate_user(self):
        """Activar un usuario previamente desactivado (primer bloque, adaptado)."""
        self.normal_user.is_active = False
        self.normal_user.save(update_fields=["is_active"])

        activate_user(user=self.normal_user, performed_by=self.admin)
        self.normal_user.refresh_from_db()
        self.assertTrue(self.normal_user.is_active)

    # Tests del segundo bloque
    def test_create_user_hashes_password_and_assigns_groups(self):
        """Creación de usuario con password hasheado y asignación de grupos."""
        group = Group.objects.create(name="Administradores")

        user = create_user(
            data={
                "username": "juan",
                "first_name": "Juan",
                "last_name": "Pérez",
                "email": "juan@example.com",
                "phone": "0999999999",
                "job_title": "Supervisor",
                "is_active": True,
                "must_change_password": True,
                "groups": [group],
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
            performed_by=self.admin,
        )

        self.assertTrue(user.check_password("StrongPass123!"))
        self.assertEqual(user.groups.count(), 1)

    def test_activate_and_deactivate_user(self):
        """Prueba combinada de activación y desactivación (segundo bloque)."""
        user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="StrongPass123!",
            is_active=True,
        )

        deactivate_user(user=user, performed_by=self.admin)
        user.refresh_from_db()
        self.assertFalse(user.is_active)

        activate_user(user=user, performed_by=self.admin)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_bootstrap_default_groups_creates_seed_roles(self):
        """Verifica que se creen los grupos por defecto."""
        bootstrap_default_groups()

        self.assertTrue(Group.objects.filter(name=DefaultGroup.ADMINISTRADORES).exists())
        self.assertTrue(Group.objects.filter(name=DefaultGroup.COORDINADORES).exists())

    def test_register_access_event_creates_log(self):
        """Registro de evento de acceso crea una entrada en UserAccessLog."""
        request = self.factory.post("/accounts/login/")
        request.META["REMOTE_ADDR"] = "127.0.0.1"
        request.META["HTTP_USER_AGENT"] = "pytest"

        register_access_event(
            request=request,
            user=self.admin,
            identifier="superadmin",
            event_type=AccessEventType.LOGIN,
            status=AccessEventStatus.SUCCESS,
            detail="Login correcto",
        )

        self.assertEqual(UserAccessLog.objects.count(), 1)