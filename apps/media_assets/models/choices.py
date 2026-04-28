from django.db import models


class PhotoClassification(models.TextChoices):
    BEFORE = "before", "Before"
    IN_PROGRESS = "in_progress", "In progress"
    FINAL = "final", "Final"