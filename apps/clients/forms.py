from django import forms
from django.utils import timezone

from .models import Client, ClientInteraction
from .models.choices import ClientStatus, ClientType


DATETIME_INPUT_FORMAT = "%Y-%m-%dT%H:%M"


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "legal_name",
            "commercial_name",
            "client_type",
            "document_number",
            "email",
            "phone",
            "alternate_phone",
            "address",
            "city",
            "state",
            "country",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        return email.strip().lower()

    def clean_legal_name(self):
        return self.cleaned_data["legal_name"].strip()

    def clean_commercial_name(self):
        return self.cleaned_data.get("commercial_name", "").strip()

    def clean_document_number(self):
        return self.cleaned_data.get("document_number", "").strip()


class ClientFilterForm(forms.Form):
    search = forms.CharField(required=False, label="Búsqueda")
    status = forms.ChoiceField(
        required=False,
        label="Estado",
        choices=[("", "Todos")] + list(ClientStatus.choices),
    )
    client_type = forms.ChoiceField(
        required=False,
        label="Tipo",
        choices=[("", "Todos")] + list(ClientType.choices),
    )


class ClientInteractionForm(forms.ModelForm):
    occurred_at = forms.DateTimeField(
        label="Fecha de interacción",
        initial=timezone.now,
        input_formats=[DATETIME_INPUT_FORMAT],
        widget=forms.DateTimeInput(
            format=DATETIME_INPUT_FORMAT,
            attrs={"type": "datetime-local"},
        ),
    )
    follow_up_at = forms.DateTimeField(
        label="Seguimiento programado",
        required=False,
        input_formats=[DATETIME_INPUT_FORMAT],
        widget=forms.DateTimeInput(
            format=DATETIME_INPUT_FORMAT,
            attrs={"type": "datetime-local"},
        ),
    )

    class Meta:
        model = ClientInteraction
        fields = [
            "interaction_type",
            "occurred_at",
            "summary",
            "description",
            "follow_up_at",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_summary(self):
        return self.cleaned_data["summary"].strip()

    def clean(self):
        cleaned_data = super().clean()
        occurred_at = cleaned_data.get("occurred_at")
        follow_up_at = cleaned_data.get("follow_up_at")

        if occurred_at and follow_up_at and follow_up_at < occurred_at:
            self.add_error(
                "follow_up_at",
                "La fecha de seguimiento no puede ser anterior a la interacción.",
            )

        return cleaned_data