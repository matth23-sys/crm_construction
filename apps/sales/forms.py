# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from apps.clients.models import Client
from apps.users.models import User
from .models import Opportunity, OpportunityStage
from .models.choices import OpportunitySource, OpportunityStatus


class OpportunityForm(forms.ModelForm):
    """
    Formulario para crear y editar oportunidades.
    """
    class Meta:
        model = Opportunity
        fields = [
            'client',
            'title',
            'description',
            'responsible',
            'estimated_value',
            'expected_close_date',
            'source',
            'internal_notes',
        ]
        widgets = {
            'expected_close_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'internal_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo clientes activos
        self.fields['client'].queryset = Client.objects.filter(is_active=True)
        # Hacer el campo responsible opcional
        self.fields['responsible'].required = False
        self.fields['responsible'].queryset = User.objects.filter(is_active=True)

    def clean_expected_close_date(self):
        date = self.cleaned_data.get('expected_close_date')
        if date:
            from django.utils import timezone
            if date < timezone.now().date():
                raise ValidationError("La fecha esperada de cierre no puede ser anterior a hoy.")
        return date


class OpportunityStageMoveForm(forms.Form):
    to_stage = forms.ModelChoiceField(
        queryset=OpportunityStage.objects.none(),
        label="Nueva etapa",
        empty_label="Selecciona una etapa",
    )
    note = forms.CharField(
        required=False,
        label="Nota",
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def __init__(self, *args, opportunity=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.opportunity = opportunity

        queryset = OpportunityStage.objects.filter(is_active=True).order_by("position")

        if opportunity is not None and getattr(opportunity, "stage_id", None):
            queryset = queryset.exclude(pk=opportunity.stage_id)

        self.fields["to_stage"].queryset = queryset


class OpportunityFilterForm(forms.Form):
    """
    Formulario para filtrar el listado de oportunidades.
    """
    search = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={'placeholder': 'Título o cliente'})
    )
    client = forms.ModelChoiceField(
        queryset=Client.objects.filter(is_active=True),
        required=False,
        label='Cliente'
    )
    responsible = forms.ChoiceField(
        required=False,
        label='Responsable',
        choices=[('', '---------')]  # Se llena dinámicamente en la vista
    )
    include_closed = forms.BooleanField(
        required=False,
        label='Incluir cerradas'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Las opciones de 'responsible' se agregan en la vista porque necesitan acceso a la base de datos
        # y no queremos consultar aquí para mantener el formulario reusable.