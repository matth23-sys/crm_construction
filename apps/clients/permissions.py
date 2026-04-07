from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect


class ClientPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Redirige a la vista de acceso denegado del módulo users
    cuando el usuario está autenticado pero no tiene permisos.
    """

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request,
                "No tienes permisos suficientes para acceder a este recurso.",
            )
            return redirect("users:access_denied")
        return super().handle_no_permission()