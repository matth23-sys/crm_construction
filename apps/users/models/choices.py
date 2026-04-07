from django.db import models


class DefaultGroup(models.TextChoices):
    ADMINISTRADORES = "Administradores", "Administradores"
    COORDINADORES = "Coordinadores", "Coordinadores"
    COMERCIAL = "Comercial", "Comercial"
    CUADRILLA = "Cuadrilla", "Cuadrilla"


class AccessEventType(models.TextChoices):
    LOGIN = "login", "Inicio de sesión"
    LOGOUT = "logout", "Cierre de sesión"
    PASSWORD_RESET_REQUEST = "password_reset_request", "Solicitud de reseteo"
    PASSWORD_RESET_COMPLETE = "password_reset_complete", "Reseteo completado"
    ACCESS_DENIED = "access_denied", "Acceso denegado"


class AccessEventStatus(models.TextChoices):
    SUCCESS = "success", "Éxito"
    FAILED = "failed", "Fallido"
    DENIED = "denied", "Denegado"
    INFO = "info", "Informativo"