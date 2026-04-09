# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.models import Group, Permission
from django.core.validators import EmailValidator

from .selectors import get_role_queryset

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    groups = forms.ModelMultipleChoiceField(
        label='Roles',
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone', 'job_title', 'is_active', 'must_change_password', 'groups'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if User.objects.filter(username__iexact=username).exists():
                raise forms.ValidationError('Este nombre de usuario ya está registrado.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Dejar en blanco para mantener la actual.'
    )
    password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    groups = forms.ModelMultipleChoiceField(
        label='Roles',
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone', 'job_title', 'is_active', 'must_change_password', 'groups'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['password1'].help_text = 'Dejar en blanco para mantener la contraseña actual.'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
            qs = User.objects.filter(email__iexact=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Este correo electrónico ya está registrado por otro usuario.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            qs = User.objects.filter(username__iexact=username)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Este nombre de usuario ya está registrado.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'job_title']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
            qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Este correo electrónico ya está registrado por otro usuario.')
        return email


class UserFilterForm(forms.Form):
    search = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre, email o usuario'
        })
    )
    is_active = forms.ChoiceField(
        label='Estado',
        choices=[('', 'Todos'), ('true', 'Activo'), ('false', 'Inactivo')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    group = forms.ModelChoiceField(
        label='Rol',
        queryset=get_role_queryset(),
        required=False,
        empty_label='Todos los roles',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class RoleForm(forms.ModelForm):
    """Formulario para crear y editar roles (grupos)."""
    
    permissions = forms.ModelMultipleChoiceField(
        label='Permisos',
        queryset=Permission.objects.select_related('content_type').order_by(
            'content_type__app_label', 'codename'
        ),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            qs = Group.objects.filter(name__iexact=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Ya existe un rol con este nombre.')
        return name


class UserPasswordResetForm(DjangoPasswordResetForm):
    """Formulario personalizado para recuperación de contraseña."""
    
    email = forms.EmailField(
        label='Correo electrónico',
        max_length=254,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo electrónico'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
        return email