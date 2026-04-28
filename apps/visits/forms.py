from django import forms
from django.utils import timezone
from .models import TechnicalVisit, ReminderDeliveryStatus, ReminderType, VisitStatus

class TechnicalVisitForm(forms.ModelForm):
    class Meta:
        model = TechnicalVisit
        fields = [
            "title", "client", "project", "responsible", "scheduled_for",
            "location", "description", "reminder_enabled", "reminder_type"
        ]
        widgets = {
            "scheduled_for": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields["scheduled_for"].initial = timezone.now()

class VisitRescheduleForm(forms.Form):
    scheduled_for = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        label="Nueva fecha y hora"
    )
    reschedule_reason = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2}),
        required=False,
        label="Motivo de reprogramación"
    )

class TechnicalVisitFilterForm(forms.Form):
    search = forms.CharField(required=False, label="Buscar")
    status = forms.ChoiceField(choices=[("", "Todos")] + list(VisitStatus.choices), required=False)
    responsible = forms.ModelChoiceField(queryset=None, required=False, label="Responsable")
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth import get_user_model
        self.fields["responsible"].queryset = get_user_model().objects.filter(is_active=True)

class VisitReminderLogFilterForm(forms.Form):
    status = forms.ChoiceField(choices=[("", "Todos")] + list(ReminderDeliveryStatus.choices), required=False)
    reminder_type = forms.ChoiceField(choices=[("", "Todos")] + list(ReminderType.choices), required=False)
    visit_title = forms.CharField(required=False, label="Título de visita")