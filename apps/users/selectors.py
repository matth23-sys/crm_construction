from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Count, Q

from .models import UserAccessLog

User = get_user_model()


def get_user_queryset():
    return User.objects.prefetch_related("groups").order_by("username")


def get_filtered_user_queryset(*, search="", is_active=None, group_name=""):
    queryset = get_user_queryset()

    if search:
        queryset = queryset.filter(
            Q(username__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(email__icontains=search)
            | Q(job_title__icontains=search)
        )

    if is_active in {"true", "false"}:
        queryset = queryset.filter(is_active=(is_active == "true"))

    if group_name:
        queryset = queryset.filter(groups__name=group_name)

    return queryset.distinct()


def get_user_by_pk(pk):
    return get_user_queryset().get(pk=pk)


def get_role_queryset():
    return Group.objects.prefetch_related("permissions").order_by("name")


def get_role_list_queryset():
    return get_role_queryset().annotate(user_count=Count("user"))


def get_access_log_queryset():
    return UserAccessLog.objects.select_related("user").order_by("-created_at")