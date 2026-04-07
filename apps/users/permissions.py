from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect

from .models.choices import AccessEventStatus, AccessEventType
from .services import register_access_event


class AppPermissionRequiredMixin(PermissionRequiredMixin):
    permission_denied_redirect_name = "users:access_denied"
    permission_denied_message = "No tienes permisos para acceder a esta página."

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        register_access_event(
            request=self.request,
            user=self.request.user,
            event_type=AccessEventType.ACCESS_DENIED,
            status=AccessEventStatus.DENIED,
            identifier=self.request.user.username,
            detail=f"Intento de acceso a {self.request.path}",
        )
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.permission_denied_redirect_name)