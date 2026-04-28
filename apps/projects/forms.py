from django import forms
from django.db.models import Q

from apps.clients.models import Client
from apps.sales.models import Opportunity
from django.contrib.auth import get_user_model

from .models import Project
from .models.choices import ProjectAssignmentRole, ProjectNoteType, ProjectStatus

User = get_user_model()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "client",
            "opportunity",
            "responsible",
            "name",
            "description",
            "location",
            "status",
            "contract_amount",
            "start_date",
            "expected_end_date",
            "actual_end_date",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "expected_end_date": forms.DateInput(attrs={"type": "date"}),
            "actual_end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["client"].queryset = Client.objects.filter(is_active=True)
        self.fields["responsible"].queryset = User.objects.filter(is_active=True)

        opportunity_queryset = Opportunity.objects.all()
        if self.instance and self.instance.pk and self.instance.opportunity_id:
            opportunity_queryset = opportunity_queryset.filter(
                Q(project__isnull=True) | Q(pk=self.instance.opportunity_id)
            )
        else:
            opportunity_queryset = opportunity_queryset.filter(project__isnull=True)

        self.fields["opportunity"].queryset = opportunity_queryset

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get("client")
        opportunity = cleaned_data.get("opportunity")
        start_date = cleaned_data.get("start_date")
        expected_end_date = cleaned_data.get("expected_end_date")
        actual_end_date = cleaned_data.get("actual_end_date")

        if client and opportunity and opportunity.client_id != client.id:
            self.add_error("opportunity", "The selected opportunity does not belong to the selected client.")

        if start_date and expected_end_date and expected_end_date < start_date:
            self.add_error("expected_end_date", "Expected end date cannot be earlier than start date.")

        if start_date and actual_end_date and actual_end_date < start_date:
            self.add_error("actual_end_date", "Actual end date cannot be earlier than start date.")

        return cleaned_data


class ProjectFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Search")
    status = forms.ChoiceField(
        required=False,
        choices=[("", "All statuses")] + list(ProjectStatus.choices),
    )
    client = forms.ModelChoiceField(
        required=False,
        queryset=Client.objects.filter(is_active=True),
    )
    responsible = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.filter(is_active=True),
    )


class ProjectAssignmentForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.none())
    role = forms.ChoiceField(choices=ProjectAssignmentRole.choices)
    notes = forms.CharField(required=False, max_length=255)

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project

        queryset = User.objects.filter(is_active=True)
        if project is not None:
            assigned_user_ids = project.assignments.filter(is_active=True).values_list("user_id", flat=True)
            queryset = queryset.exclude(id__in=assigned_user_ids)

        self.fields["user"].queryset = queryset


class ProjectNoteForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Internal note",
    )
    note_type = forms.ChoiceField(
        choices=ProjectNoteType.choices,
        initial=ProjectNoteType.INTERNAL,
    )