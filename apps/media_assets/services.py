# -*- coding: utf-8 -*-
from django.db import transaction

from .models import ProjectPhoto


def _set_actor_stamps(instance, actor, is_create=False):
    if actor is None or not getattr(actor, "is_authenticated", False):
        return

    if is_create and hasattr(instance, "created_by"):
        instance.created_by = actor

    if hasattr(instance, "updated_by"):
        instance.updated_by = actor


def _populate_file_metadata(photo, uploaded_file):
    photo.original_filename = getattr(uploaded_file, "name", "") or ""
    photo.mime_type = getattr(uploaded_file, "content_type", "") or ""
    photo.file_size = getattr(uploaded_file, "size", 0) or 0


@transaction.atomic
def create_project_photo(
    *,
    project,
    image,
    classification,
    actor,
    title="",
    description="",
    taken_at=None,
):
    photo = ProjectPhoto(
        project=project,
        image=image,
        classification=classification,
        title=(title or "").strip(),
        description=(description or "").strip(),
        taken_at=taken_at,
    )
    _populate_file_metadata(photo, image)
    _set_actor_stamps(photo, actor, is_create=True)

    photo.full_clean()
    photo.save()
    return photo


@transaction.atomic
def replace_project_photo(
    *,
    photo,
    image,
    actor,
    classification,
    title="",
    description="",
    taken_at=None,
):
    old_storage = photo.image.storage if photo.image else None
    old_name = photo.image.name if photo.image else ""

    photo.image = image
    photo.classification = classification
    photo.title = (title or "").strip()
    photo.description = (description or "").strip()
    photo.taken_at = taken_at

    _populate_file_metadata(photo, image)
    _set_actor_stamps(photo, actor, is_create=False)

    photo.full_clean()
    photo.save()

    if old_storage and old_name and old_name != photo.image.name:
        transaction.on_commit(
            lambda: old_storage.delete(old_name)
            if old_storage.exists(old_name)
            else None
        )

    return photo


@transaction.atomic
def delete_project_photo(*, photo):
    storage = photo.image.storage if photo.image else None
    file_name = photo.image.name if photo.image else ""

    photo.delete()

    if storage and file_name:
        transaction.on_commit(
            lambda: storage.delete(file_name) if storage.exists(file_name) else None
        )