from django.db import models


class ClientStatus(models.TextChoices):
    """Estados del cliente."""
    ACTIVE = "active", "Activo"
    INACTIVE = "inactive", "Inactivo"
    LEAD = "lead", "Prospecto"


class ClientType(models.TextChoices):
    COMPANY = "company", "Empresa"
    INDIVIDUAL = "individual", "Persona natural"


class InteractionType(models.TextChoices):
    """Tipos de interacción con el cliente."""
    CALL = "call", "Llamada"
    EMAIL = "email", "Correo"
    WHATSAPP = "whatsapp", "WhatsApp"
    MEETING = "meeting", "Reunión"
    VISIT = "visit", "Visita"
    NOTE = "note", "Nota"
    OTHER = "other", "Otro"