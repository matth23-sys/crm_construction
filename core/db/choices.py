from django.db import models


class ActiveInactiveChoices(models.TextChoices):
    ACTIVE = "active", "Activo"
    INACTIVE = "inactive", "Inactivo"


class YesNoChoices(models.TextChoices):
    YES = "yes", "Sí"
    NO = "no", "No"