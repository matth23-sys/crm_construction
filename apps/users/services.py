from __future__ import annotations

from typing import Iterable

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import transaction
from django.db.models import Q

from .models import UserAccessLog
from .models.choices import AccessEventStatus, AccessEventType, DefaultGroup

User = get_user_model()


DEFAULT_GROUP_PERMISSIONS = {
    DefaultGroup.ADMINISTRADORES: [
        "users.view_user",
        "users.add_user",
        "users.change_user",
        "users.delete_user",
        "users.activate_user",
        "users.deactivate_user",
        "users.assign_user_groups",
        "users.view_user_access_logs",
        "users.view_useraccesslog",
        "auth.view_group",
        "auth.add_group",
        "auth.change_group",
        "auth.delete_group",
    ],
    DefaultGroup.COORDINADORES: [
        "users.view_user",
        "users.add_user",
        "users.change_user",
        "users.activate_user",
        "users.deactivate_user",
        "users.assign_user_groups",
        "auth.view_group",
    ],
    DefaultGroup.COMERCIAL: [],
    DefaultGroup.CUADRILLA: [],
}


def _extract_permission_queryset(permission_codes: Iterable[str]):
    query = Q()
    for permission_code in permission_codes:
        app_label, codename = permission_code.split(".", 1)
        query |= Q(content_type__app_label=app_label, codename=codename)

    if not query:
        return Permission.objects.none()

    return Permission.objects.filter(query)


def _get_request_ip(request) -> str:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


@transaction.atomic
def create_user(*, data: dict, performed_by=None):
    groups = data.pop("groups", [])
    raw_password = data.pop("password1")
    data.pop("password2", None)

    user = User(**data)
    user.set_password(raw_password)
    user.full_clean()
    user.save()

    if groups:
        user.groups.set(groups)

    return user


@transaction.atomic
def update_user(*, user: User, data: dict, performed_by=None):
    groups = data.pop("groups", None)

    for field, value in data.items():
        setattr(user, field, value)

    user.full_clean()
    user.save()

    if groups is not None:
        user.groups.set(groups)

    return user


@transaction.atomic
def update_profile(*, user: User, data: dict):
    allowed_fields = {"first_name", "last_name", "email", "phone", "job_title"}

    for field, value in data.items():
        if field in allowed_fields:
            setattr(user, field, value)

    user.full_clean()
    user.save()
    return user


@transaction.atomic
def activate_user(*, user: User, performed_by=None):
    user.is_active = True
    user.save(update_fields=["is_active", "updated_at"])
    return user


@transaction.atomic
def deactivate_user(*, user: User, performed_by=None):
    if performed_by and performed_by.pk == user.pk:
        raise ValueError("No puedes desactivarte a ti mismo.")

    user.is_active = False
    user.save(update_fields=["is_active", "updated_at"])
    return user


@transaction.atomic
def create_role(*, data: dict):
    permissions = data.pop("permissions", [])
    group = Group.objects.create(name=data["name"])
    if permissions:
        group.permissions.set(permissions)
    return group


@transaction.atomic
def update_role(*, group: Group, data: dict):
    permissions = data.pop("permissions", None)
    group.name = data["name"]
    group.save(update_fields=["name"])

    if permissions is not None:
        group.permissions.set(permissions)

    return group


def bootstrap_default_groups():
    for group_name, permission_codes in DEFAULT_GROUP_PERMISSIONS.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = _extract_permission_queryset(permission_codes)
        group.permissions.set(permissions)


def register_access_event(
    *,
    request,
    event_type: str,
    status: str = AccessEventStatus.INFO,
    user=None,
    identifier: str = "",
    detail: str = "",
    metadata: dict | None = None,
):
    metadata = metadata or {}

    return UserAccessLog.objects.create(
        user=user if getattr(user, "is_authenticated", False) else None,
        identifier=identifier,
        event_type=event_type,
        status=status,
        ip_address=_get_request_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        request_id=getattr(request, "request_id", "") or request.META.get("HTTP_X_REQUEST_ID", ""),
        detail=detail,
        metadata=metadata,
    )