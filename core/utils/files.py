from pathlib import Path
from uuid import uuid4

from django.utils import timezone
from django.utils.text import slugify


def clean_filename(filename):
    path = Path(filename)
    stem = slugify(path.stem) or "file"
    return f"{stem}{path.suffix.lower()}"


def build_dated_upload_path(filename, base_dir):
    cleaned = clean_filename(filename)
    ext = Path(cleaned).suffix.lower()
    stem = Path(cleaned).stem
    today = timezone.localdate()

    return (
        f"{base_dir}/"
        f"{today:%Y/%m/%d}/"
        f"{stem}-{uuid4().hex}{ext}"
    )