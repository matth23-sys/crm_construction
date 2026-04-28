from django.db import models
from django.conf import settings
from .choices import VisitStatus, ReminderType, ReminderDeliveryStatus
from django.db.models import Q

class TechnicalVisit(models.Model):
    title = models.CharField(max_length=200)
    client = models.ForeignKey("clients.Client", on_delete=models.PROTECT, related_name="technical_visits")
    project = models.ForeignKey("projects.Project", on_delete=models.PROTECT, null=True, blank=True, related_name="technical_visits")
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="assigned_visits")
    scheduled_for = models.DateTimeField()
    location = models.TextField(blank=True)
    description = models.TextField(blank=True)   # ✅ este campo existe ahora
    status = models.CharField(max_length=20, choices=VisitStatus.choices, default=VisitStatus.SCHEDULED)
    reminder_enabled = models.BooleanField(default=True)
    reminder_type = models.CharField(max_length=20, choices=ReminderType.choices, default=ReminderType.DAY_BEFORE)  # ✅ existe

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
    execution_date = models.DateField(
    null=True,
    blank=True,
    db_index=True,
    help_text="Fecha lógica de ejecución usada para evitar recordatorios duplicados.",
)


class Meta:
    ordering = ["-created_at"]
    constraints = [
        models.UniqueConstraint(
            fields=["visit", "reminder_type", "execution_date"],
            condition=Q(status=ReminderDeliveryStatus.SENT),
            name="uniq_sent_visit_reminder_execution_date",
        )
    ]