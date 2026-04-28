from django.db import models


class NotificationChannel(models.TextChoices):
    EMAIL = "email", "Email"


class NotificationTemplateKey(models.TextChoices):
    VISIT_DAY_BEFORE = "visit_day_before", "Visit day before"
    VISIT_SAME_DAY = "visit_same_day", "Visit same day"