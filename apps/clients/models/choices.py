from django.db import models


class ClientStatus(models.TextChoices):
    ACTIVE = "active", "Activo"
    INACTIVE = "inactive", "Inactivo"


class ClientType(models.TextChoices):
    COMPANY = "company", "Empresa"
    INDIVIDUAL = "individual", "Persona natural"


class InteractionType(models.TextChoices):
    CALL = "call", "Llamada"
    EMAIL = "email", "Correo"
    WHATSAPP = "whatsapp", "WhatsApp"
    MEETING = "meeting", "Reunión"
    VISIT = "visit", "Visita"
    NOTE = "note", "Nota"
    OTHER = "other", "Otro"