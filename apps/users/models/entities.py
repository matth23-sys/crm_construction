import uuid

from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

from core.db.base import TimeStampedModel
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
    email = models.EmailField("correo electrónico", unique=True)
    phone = models.CharField(
        "teléfono",
        max_length=20,
        blank=True,
        validators=[validate_phone_number],
    )
    job_title = models.CharField("cargo", max_length=150, blank=True)

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