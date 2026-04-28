from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

class VisitsPermissionRequiredMixin(PermissionRequiredMixin):
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("No tienes permiso para acceder a esta sección.")
        return super().handle_no_permission()