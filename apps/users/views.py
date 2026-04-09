# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import (
    UserCreateForm,
    UserUpdateForm,
    UserProfileForm,
    UserFilterForm,
    RoleForm,
)
from .models.choices import AccessEventStatus, AccessEventType
from .permissions import AppPermissionRequiredMixin
from .selectors import (
    get_access_log_queryset,
    get_filtered_user_queryset,
    get_role_list_queryset,
    get_role_queryset,
)
from .services import (
    activate_user,
    create_role,
    create_user,
    deactivate_user,
    register_access_event,
    update_profile,
    update_role,
    update_user,
)

User = get_user_model()


class CRMLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True
    form_class = AuthenticationForm  # ← Usar AuthenticationForm de Django

    def form_valid(self, form):
        response = super().form_valid(form)
        register_access_event(
            request=self.request,
            user=form.get_user(),
            identifier=form.get_user().username,
            event_type=AccessEventType.LOGIN,
            status=AccessEventStatus.SUCCESS,
            detail="Inicio de sesión correcto.",
        )
        return response

    def form_invalid(self, form):
        identifier = self.request.POST.get("username", "").strip()
        register_access_event(
            request=self.request,
            identifier=identifier,
            event_type=AccessEventType.LOGIN,
            status=AccessEventStatus.FAILED,
            detail="Credenciales inválidas.",
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return self.get_redirect_url() or "/dashboard/"


class CRMLogoutView(LogoutView):
    next_page = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            register_access_event(
                request=request,
                user=request.user,
                identifier=request.user.username,
                event_type=AccessEventType.LOGOUT,
                status=AccessEventStatus.SUCCESS,
                detail="Cierre de sesión.",
            )
        return super().dispatch(request, *args, **kwargs)


class CRMPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    subject_template_name = "registration/password_reset_subject.txt"
    form_class = PasswordResetForm  # ← Usar PasswordResetForm de Django
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        register_access_event(
            request=self.request,
            identifier=form.cleaned_data["email"].strip().lower(),
            event_type=AccessEventType.PASSWORD_RESET_REQUEST,
            status=AccessEventStatus.INFO,
            detail="Solicitud de recuperación de acceso.",
        )
        return super().form_valid(form)


class CRMPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class CRMPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")

    def form_valid(self, form):
        response = super().form_valid(form)
        register_access_event(
            request=self.request,
            user=self.user,
            identifier=getattr(self.user, "username", ""),
            event_type=AccessEventType.PASSWORD_RESET_COMPLETE,
            status=AccessEventStatus.SUCCESS,
            detail="Contraseña restablecida correctamente.",
        )
        return response


class CRMPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"


class ProfileView(generic.UpdateView):
    template_name = "users/profile.html"
    form_class = UserProfileForm  # ← Corregido: UserProfileForm en lugar de ProfileForm
    success_url = reverse_lazy("users:profile")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        update_profile(user=self.request.user, data=form.cleaned_data)
        messages.success(self.request, "Perfil actualizado correctamente.")
        return HttpResponseRedirect(self.get_success_url())


class UserListView(AppPermissionRequiredMixin, generic.ListView):
    template_name = "users/list.html"
    context_object_name = "users"
    paginate_by = 20
    permission_required = "users.view_user"

    def get_queryset(self):
        return get_filtered_user_queryset(
            search=self.request.GET.get("search", "").strip(),
            is_active=self.request.GET.get("is_active", "").strip().lower(),
            group_name=self.request.GET.get("group", "").strip(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = UserFilterForm(self.request.GET or None)  # ← Agregado
        context["search"] = self.request.GET.get("search", "")
        context["selected_group"] = self.request.GET.get("group", "")
        context["selected_is_active"] = self.request.GET.get("is_active", "")
        return context


class UserDetailView(AppPermissionRequiredMixin, generic.DetailView):
    model = User
    template_name = "users/detail.html"
    context_object_name = "managed_user"
    permission_required = "users.view_user"


class UserCreateView(AppPermissionRequiredMixin, generic.FormView):
    template_name = "users/form.html"
    form_class = UserCreateForm
    permission_required = "users.add_user"
    success_url = reverse_lazy("users:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear usuario"
        return context

    def form_valid(self, form):
        create_user(data=form.cleaned_data, performed_by=self.request.user)
        messages.success(self.request, "Usuario creado correctamente.")
        return super().form_valid(form)


class UserUpdateView(AppPermissionRequiredMixin, generic.UpdateView):
    model = User
    template_name = "users/form.html"
    form_class = UserUpdateForm
    context_object_name = "managed_user"
    permission_required = "users.change_user"
    success_url = reverse_lazy("users:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar usuario"
        return context

    def form_valid(self, form):
        update_user(user=self.object, data=form.cleaned_data, performed_by=self.request.user)
        messages.success(self.request, "Usuario actualizado correctamente.")
        return HttpResponseRedirect(self.get_success_url())


class UserActivateView(AppPermissionRequiredMixin, View):
    permission_required = "users.activate_user"

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        activate_user(user=user, performed_by=request.user)
        messages.success(request, "Usuario activado correctamente.")
        return redirect("users:detail", pk=user.pk)


class UserDeactivateView(AppPermissionRequiredMixin, View):
    permission_required = "users.deactivate_user"

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        try:
            deactivate_user(user=user, performed_by=request.user)
            messages.success(request, "Usuario desactivado correctamente.")
        except ValueError as exc:
            messages.error(request, str(exc))
        return redirect("users:detail", pk=user.pk)


class RoleListView(AppPermissionRequiredMixin, generic.ListView):
    template_name = "users/role_list.html"
    context_object_name = "roles"
    permission_required = "auth.view_group"

    def get_queryset(self):
        return get_role_list_queryset()


class RoleCreateView(AppPermissionRequiredMixin, generic.FormView):
    template_name = "users/role_form.html"
    form_class = RoleForm
    permission_required = "auth.add_group"
    success_url = reverse_lazy("users:role_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear rol"
        return context

    def form_valid(self, form):
        create_role(data=form.cleaned_data)
        messages.success(self.request, "Rol creado correctamente.")
        return super().form_valid(form)


class RoleUpdateView(AppPermissionRequiredMixin, generic.UpdateView):
    model = Group
    template_name = "users/role_form.html"
    form_class = RoleForm
    context_object_name = "role"
    permission_required = "auth.change_group"
    success_url = reverse_lazy("users:role_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar rol"
        return context

    def form_valid(self, form):
        update_role(group=self.object, data=form.cleaned_data)
        messages.success(self.request, "Rol actualizado correctamente.")
        return HttpResponseRedirect(self.get_success_url())


class AccessLogListView(AppPermissionRequiredMixin, generic.ListView):
    template_name = "users/access_log_list.html"
    context_object_name = "logs"
    paginate_by = 50
    permission_required = "users.view_user_access_logs"

    def get_queryset(self):
        return get_access_log_queryset()


class AccessDeniedView(generic.TemplateView):
    template_name = "users/access_denied.html"


def permission_denied_view(request, exception=None):
    return AccessDeniedView.as_view()(request)