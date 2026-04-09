# -*- coding: utf-8 -*-
import uuid

from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

from core.db.base import TimeStampedModel, UUIDModel
from core.validators import validate_phone_number


class UserManager(DjangoUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
        return super().create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return super().create_superuser(
            username=username,
            email=email,
            password=password,
            **extra_fields,
        )


class User(AbstractUser, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField("correo electronico", unique=True)
    phone = models.CharField(
        "telefono",
        max_length=20,
        blank=True,
        validators=[validate_phone_number],
    )
    job_title = models.CharField("cargo", max_length=150, blank=True)
    must_change_password = models.BooleanField(
        "debe cambiar contraseña",
        default=False,
        help_text="Obligar al usuario a cambiar su contraseña en el próximo inicio de sesión"
    )

    objects = UserManager()

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ("username",)

    @property
    def full_name(self):
        value = f"{self.first_name} {self.last_name}".strip()
        return value or self.username

    def __str__(self):
        return self.full_name


class UserAccessLog(UUIDModel, TimeStampedModel):
    """Registro de eventos de acceso y seguridad del usuario."""

    EVENT_TYPES = [
        ('login_success', 'Login exitoso'),
        ('login_failed', 'Login fallido'),
        ('logout', 'Logout'),
        ('password_reset_request', 'Solicitud de recuperacion'),
        ('password_reset_complete', 'Recuperacion completada'),
        ('access_denied', 'Acceso denegado'),
    ]

    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='access_logs',
        verbose_name='usuario'
    )
    identifier_used = models.CharField(
        'identificador usado',
        max_length=255,
        blank=True,
        help_text='Email o username usado en el intento'
    )
    event_type = models.CharField(
        'tipo de evento',
        max_length=50,
        choices=EVENT_TYPES,
        db_index=True
    )
    event_status = models.CharField(
        'estado del evento',
        max_length=20,
        default='success',
        db_index=True
    )
    ip_address = models.GenericIPAddressField(
        'direccion IP',
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        'User Agent',
        blank=True
    )
    request_id = models.CharField(
        'Request ID',
        max_length=100,
        blank=True,
        db_index=True
    )
    details = models.JSONField(
        'detalles adicionales',
        default=dict,
        blank=True
    )

    class Meta:
        db_table = 'user_access_logs'
        verbose_name = 'log de acceso'
        verbose_name_plural = 'logs de acceso'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['event_type', '-created_at']),
            models.Index(fields=['ip_address']),
        ]

    def __str__(self):
        user_str = self.user.email if self.user else self.identifier_used or 'Usuario desconocido'
        return f'{self.get_event_type_display()} - {user_str} - {self.created_at.strftime("%Y-%m-%d %H:%M")}'