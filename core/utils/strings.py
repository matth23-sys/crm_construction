import re
import unicodedata

from django.utils.text import slugify


def compact_spaces(value):
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()


def normalize_text(value):
    if not value:
        return ""

    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    return compact_spaces(value).lower()


def safe_slug(value, fallback="item"):
    slug = slugify(value or "")
    return slug or fallback