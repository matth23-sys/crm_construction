from django.db import models

class VisitStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Programada"
    COMPLETED = "completed", "Completada"
    CANCELLED = "cancelled", "Cancelada"
    RESCHEDULED = "rescheduled", "Reprogramada"

class ReminderType(models.TextChoices):
    DAY_BEFORE = "day_before", "One day before"
    SAME_DAY = "same_day", "Same day"
    TWO_HOURS_BEFORE = "two_hours_before", "Two hours before"

class ReminderDeliveryStatus(models.TextChoices):
    PENDING = "pending", "Pendiente"
    SENT = "sent", "Enviado"
    FAILED = "failed", "Error"