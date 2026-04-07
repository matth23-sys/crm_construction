from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError

from .selectors import get_role_queryset

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Usuario"}),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"}),
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "Tu cuenta está desactivada. Contacta al administrador.",
                code="inactive",
            )


class UserCreateForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(),
        required=False,
        label="Roles",
        widget=forms.CheckboxSelectMultiple,
    )
    must_change_password = forms.BooleanField(
        required=False,
        initial=True,
        label="Forzar cambio de contraseña en el primer acceso",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "job_title",
            "is_active",
            "groups",
            "must_change_password",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["groups"].queryset = get_role_queryset()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ya existe un usuario con este correo.")
        return email


class UserUpdateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(),
        required=False,
        label="Roles",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "job_title",
            "is_active",
            "must_change_password",
            "groups",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["groups"].queryset = get_role_queryset()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if queryset.exists():
            raise ValidationError("Ya existe un usuario con este correo.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "job_title")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        queryset = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if queryset.exists():
            raise ValidationError("Ya existe un usuario con este correo.")
        return email


class RoleForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),
        required=False,
        label="Permisos",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Group
        fields = ("name", "permissions")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["permissions"].queryset = Permission.objects.select_related(
            "content_type"
        ).order_by("content_type__app_label", "codename")


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "Correo registrado"}),
    )