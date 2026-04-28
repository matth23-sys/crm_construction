from django.db import models
from django.conf import settings
from django.utils import timezone

class ReminderType(models.TextChoices):
    DAY_BEFORE = "day_before", "Un día antes"
    SAME_DAY = "same_day", "El mismo día"
    # Puedes agregar más si lo necesitas

class ReminderDeliveryStatus(models.TextChoices):
    PENDING = "pending", "Pendiente"
    SENT = "sent", "Enviado"
    FAILED = "failed", "Error"

class VisitStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Programada"
    COMPLETED = "completed", "Completada"
    CANCELLED = "cancelled", "Cancelada"
    RESCHEDULED = "rescheduled", "Reprogramada"

class TechnicalVisit(models.Model):
    title = models.CharField(max_length=200)
    client = models.ForeignKey("clients.Client", on_delete=models.PROTECT, related_name="technical_visits")
    project = models.ForeignKey("projects.Project", on_delete=models.PROTECT, null=True, blank=True, related_name="technical_visits")
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="assigned_visits")
    scheduled_for = models.DateTimeField()
    location = models.TextField(blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=VisitStatus.choices, default=VisitStatus.SCHEDULED)
    reminder_enabled = models.BooleanField(default=True)
    reminder_type = models.CharField(max_length=20, choices=ReminderType.choices, default=ReminderType.DAY_BEFORE)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class VisitReminderLog(models.Model):
    visit = models.ForeignKey(TechnicalVisit, on_delete=models.CASCADE, related_name="reminder_logs")
    reminder_type = models.CharField(max_length=20, choices=ReminderType.choices)
    status = models.CharField(max_length=20, choices=ReminderDeliveryStatus.choices, default=ReminderDeliveryStatus.PENDING)
    recipient_email = models.EmailField()
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]