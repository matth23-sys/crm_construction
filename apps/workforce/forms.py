from django import forms

from .models.choices import (
    WorkforceMilestoneAction,
    get_available_actions_for_status,
)


class WorkforceProjectFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Project, client, location...",
            }
        ),
    )
    status = forms.ChoiceField(
        required=False,
        label="Status",
        choices=(
            ("", "All"),
            ("pending", "Pending"),
            ("in_progress", "In progress"),
            ("completed", "Completed"),
        ),
    )


class FieldNoteForm(forms.Form):
    body = forms.CharField(
        label="Field note",
        max_length=2000,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Describe the field update, progress, issue, or completed task.",
            }
        ),
    )

    def clean_body(self):
        body = self.cleaned_data["body"].strip()
        if not body:
            raise forms.ValidationError("The field note cannot be empty.")
        return body


class WorkforceMilestoneUpdateForm(forms.Form):
    action = forms.ChoiceField(
        label="Allowed milestone",
        choices=(),
    )

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project

        available_actions = []
        if project is not None:
            available_actions = get_available_actions_for_status(project.status)

        self.fields["action"].choices = [
            (action.value, action.label)
            for action in available_actions
        ]

    def clean_action(self):
        action = self.cleaned_data["action"]

        if not self.project:
            raise forms.ValidationError("Project context is required.")

        allowed_values = {
            choice[0]
            for choice in self.fields["action"].choices
        }

        if action not in allowed_values:
            raise forms.ValidationError("This milestone transition is not allowed.")
        return action