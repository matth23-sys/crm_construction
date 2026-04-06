class DomainError(Exception):
    """Excepción base para errores de dominio del proyecto."""


class BusinessRuleViolation(DomainError):
    """Se lanza cuando una regla de negocio es violada."""


class NotificationError(DomainError):
    """Se lanza cuando falla un envío de notificación."""


class InvalidFileError(DomainError):
    """Se lanza cuando un archivo no cumple reglas del sistema."""