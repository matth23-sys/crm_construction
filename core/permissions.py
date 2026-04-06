from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class ActiveUserRequiredMixin(LoginRequiredMixin):
    """Exige usuario autenticado y activo."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_active:
            raise PermissionDenied("Tu usuario está inactivo.")
        return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin(ActiveUserRequiredMixin, UserPassesTestMixin):
    """Exige usuario staff."""

    def test_func(self):
        return self.request.user.is_staff


class SuperuserRequiredMixin(ActiveUserRequiredMixin, UserPassesTestMixin):
    """Exige superusuario."""

    def test_func(self):
        return self.request.user.is_superuser


def user_has_any_perm(user, permissions):
    if not user.is_authenticated:
        return False
    return any(user.has_perm(permission) for permission in permissions)