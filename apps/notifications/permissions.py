from django.contrib.auth.mixins import PermissionRequiredMixin


class NotificationPermissionRequiredMixin(PermissionRequiredMixin):
    raise_exception = True