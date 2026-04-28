# -*- coding: utf-8 -*-
import os
import uuid
from pathlib import Path

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify

from apps.projects.models import Project
from core.db.base import UUIDModel, TimeStampedModel, UserStampedModel

from .choices import PhotoClassification


ALLOWED_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]


def project_photo_upload_to(instance, filename):
    extension = Path(filename).suffix.lower() or ".jpg"
    base_name = slugify(Path(filename).stem)[:60] or "project-photo"

    return (
        f"projects/{instance.project_id}/photos/"
        f"{instance.classification}/{uuid.uuid4().hex}_{base_name}{extension}"
    )


class ProjectPhoto(UUIDModel, TimeStampedModel, UserStampedModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    image = models.ImageField(
        upload_to=project_photo_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)],
    )
    classification = models.CharField(
        max_length=20,
        choices=PhotoClassification.choices,
        default=PhotoClassification.IN_PROGRESS,
    )
    title = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    taken_at = models.DateTimeField(null=True, blank=True)

    original_filename = models.CharField(max_length=255, blank=True)
    mime_type = models.CharField(max_length=100, blank=True)
    file_size = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ("-taken_at", "-created_at")
        permissions = (
            ("view_project_gallery", "Can view project gallery"),
            ("upload_projectphoto", "Can upload project photos"),
            ("replace_projectphoto", "Can replace project photos"),
        )

    def __str__(self):
        return f"{self.project.name} - {self.get_classification_display()} - {self.filename}"

    @property
    def filename(self):
        if not self.image:
            return ""
        return os.path.basename(self.image.name)

    @property
    def uploaded_by(self):
        return getattr(self, "created_by", None)