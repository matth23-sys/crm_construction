import re
from pathlib import Path

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.constants import MAX_UPLOAD_SIZE_MB

PHONE_REGEX = re.compile(r"^\+?[0-9()\-\s]{7,20}$")
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_phone_number(value):
    if not value:
        return

    if not PHONE_REGEX.match(value):
        raise ValidationError(_("Ingrese un número de teléfono válido."))


def validate_file_size(value, max_size_mb=MAX_UPLOAD_SIZE_MB):
    size_in_mb = value.size / (1024 * 1024)
    if size_in_mb > max_size_mb:
        raise ValidationError(
            _(f"El archivo excede el tamaño máximo permitido de {max_size_mb} MB.")
        )


def validate_image_extension(value):
    extension = Path(value.name).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_EXTENSIONS))
        raise ValidationError(_(f"Formato no permitido. Use: {allowed}"))