from django.conf import settings
from django.core.validators import EmailValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.db.base import BaseModel

from .choices import ClientStatus, ClientType, InteractionType


class Client(BaseModel):
    legal_name = models.CharField(
        "razón social / nombre completo",
        max_length=255,
        db_index=True,
    )
    commercial_name = models.CharField(
        "nombre comercial",
        max_length=255,
        blank=True,
        db_index=True,
    )
    client_type = models.CharField(
        "tipo de cliente",
        max_length=20,
        choices=ClientType.choices,
        default=ClientType.COMPANY,
        db_index=True,
    )
    document_number = models.CharField(
        "documento / RUC",
        max_length=30,
        blank=True,
        db_index=True,
    )
    email = models.EmailField(
        "correo electrónico",
        blank=True,
        validators=[EmailValidator()],
        db_index=True,
    )
    phone = models.CharField(
        "teléfono principal",
        max_length=30,
        blank=True,
        db_index=True,
    )
    alternate_phone = models.CharField(
        "teléfono alterno",
        max_length=30,
        blank=True,
    )
    address = models.CharField(
        "dirección",
        max_length=255,
        blank=True,
    )
    city = models.CharField(
        "ciudad",
        max_length=120,
        blank=True,
    )
    state = models.CharField(
        "provincia / estado",
        max_length=120,
        blank=True,
    )
    country = models.CharField(
        "país",
        max_length=120,
        blank=True,
        default="Ecuador",
    )
    notes = models.TextField(
        "notas internas",
        blank=True,
    )

    status = models.CharField(
        "estado",
        max_length=20,
        choices=ClientStatus.choices,
        default=ClientStatus.ACTIVE,
        db_index=True,
    )
    is_active = models.BooleanField(
        "activo",
        default=True,
        db_index=True,
    )
    deactivated_at = models.DateTimeField(
        "desactivado el",
        null=True,
        blank=True,
    )
    deactivated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deactivated_clients",
        verbose_name="desactivado por",
    )

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        ordering = ("legal_name", "commercial_name")
        permissions = (
            ("deactivate_client", "Can deactivate client"),
            ("reactivate_client", "Can reactivate client"),
        )

    def __str__(self) -> str:
        return self.display_name

    @property
    def display_name(self) -> str:
        return self.commercial_name.strip() if self.commercial_name else self.legal_name

    def clean(self):
        if self.email:
            self.email = self.email.strip().lower()

        if self.legal_name:
            self.legal_name = self.legal_name.strip()

        if self.commercial_name:
            self.commercial_name = self.commercial_name.strip()

        if self.document_number:
            self.document_number = self.document_number.strip()

        if self.phone:
            self.phone = self.phone.strip()

        if self.alternate_phone:
            self.alternate_phone = self.alternate_phone.strip()

    def deactivate(self, user=None):
        self.is_active = False
        self.status = ClientStatus.INACTIVE
        self.deactivated_at = timezone.now()
        if user is not None:
            self.deactivated_by = user

    def reactivate(self):
        self.is_active = True
        self.status = ClientStatus.ACTIVE
        self.deactivated_at = None
        self.deactivated_by = None

    def get_absolute_url(self):
        return reverse("clients:detail", kwargs={"pk": self.pk})


class ClientInteraction(BaseModel):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="interactions",
        verbose_name="cliente",
    )
    interaction_type = models.CharField(
        "tipo de interacción",
        max_length=20,
        choices=InteractionType.choices,
        db_index=True,
    )
    occurred_at = models.DateTimeField(
        "fecha de interacción",
        default=timezone.now,
        db_index=True,
    )
    summary = models.CharField(
        "resumen",
        max_length=255,
    )
    description = models.TextField(
        "detalle",
        blank=True,
    )
    follow_up_at = models.DateTimeField(
        "seguimiento programado",
        null=True,
        blank=True,
        db_index=True,
    )
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registered_client_interactions",
        verbose_name="registrado por",
    )

    class Meta:
        verbose_name = "interacción de cliente"
        verbose_name_plural = "interacciones de clientes"
        ordering = ("-occurred_at", "-created_at")

    def __str__(self) -> str:
        return f"{self.client.display_name} - {self.get_interaction_type_display()}"