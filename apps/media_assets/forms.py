# -*- coding: utf-8 -*-
from pathlib import Path

from PIL import Image

from django import forms
from django.core.exceptions import ValidationError

from .models import PhotoClassification, ProjectPhoto


MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


class ImageValidationMixin:
    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image

        extension = Path(image.name).suffix.lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise ValidationError(
                "Allowed image types are JPG, JPEG, PNG and WEBP."
            )

        content_type = getattr(image, "content_type", "")
        if content_type and content_type not in ALLOWED_CONTENT_TYPES:
            raise ValidationError(
                "Invalid image MIME type. Use JPG, PNG or WEBP."
            )

        if image.size > MAX_IMAGE_SIZE_BYTES:
            raise ValidationError(
                "Image exceeds the maximum allowed size of 10 MB."
            )

        try:
            image.open()
            Image.open(image).verify()
            image.seek(0)
        except Exception as exc:
            raise ValidationError("Upload a valid image file.") from exc

        return image


class BaseProjectPhotoForm(ImageValidationMixin, forms.ModelForm):
    class Meta:
        model = ProjectPhoto
        fields = ["image", "classification", "title", "description", "taken_at"]
        widgets = {
            "taken_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop("project", None)
        super().__init__(*args, **kwargs)
        self.fields["classification"].choices = PhotoClassification.choices

    def clean_title(self):
        return (self.cleaned_data.get("title") or "").strip()

    def clean_description(self):
        return (self.cleaned_data.get("description") or "").strip()


class ProjectPhotoUploadForm(BaseProjectPhotoForm):
    pass


class ProjectPhotoReplaceForm(BaseProjectPhotoForm):
    pass


class ProjectPhotoFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Search")
    classification = forms.ChoiceField(required=False, label="Classification")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["classification"].choices = [("", "All")] + list(
            PhotoClassification.choices
        )