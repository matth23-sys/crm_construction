# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from apps.billing.models import AccountReceivable, Payment
from apps.billing.models.choices import AccountReceivableStatus, PaymentMethod
from apps.clients.models import Client
from apps.projects.models import Project
from apps.billing.models import AccountReceivable, Payment, Expense
from apps.billing.models.choices import AccountReceivableStatus, PaymentMethod, ExpenseCategory, ExpenseStatus

class AccountReceivableForm(forms.ModelForm):
    class Meta:
        model = AccountReceivable
        fields = [
            "client",
            "project",
            "title",
            "invoice_number",
            "description",
            "total_amount",
            "issued_date",
            "due_date",
            "notes",
        ]
        widgets = {
            "issued_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["client"].queryset = Client.objects.all().order_by("legal_name")
        self.fields["project"].queryset = Project.objects.select_related("client").all().order_by("-created_at")
        self.fields["project"].required = False

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get("client")
        project = cleaned_data.get("project")
        issued_date = cleaned_data.get("issued_date")
        due_date = cleaned_data.get("due_date")

        if project and client and project.client_id != client.id:
            raise ValidationError("The selected project does not belong to the selected client.")

        if issued_date and due_date and due_date < issued_date:
            self.add_error("due_date", "Due date cannot be earlier than issued date.")

        return cleaned_data


class AccountReceivableFilterForm(forms.Form):
    search = forms.CharField(required=False, label="Search")
    status = forms.ChoiceField(
        required=False,
        choices=[("", "All statuses")] + list(AccountReceivableStatus.choices),
    )
    client = forms.ModelChoiceField(
        required=False,
        queryset=Client.objects.all().order_by("legal_name"),
    )
    project = forms.ModelChoiceField(
        required=False,
        queryset=Project.objects.all().order_by("-created_at"),
    )
    due_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    due_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    only_overdue = forms.BooleanField(required=False)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            "amount",
            "payment_date",
            "method",
            "reference_number",
            "receipt_file",
            "notes",
        ]
        widgets = {
            "payment_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop("account", None)
        super().__init__(*args, **kwargs)

        self.fields["method"].choices = PaymentMethod.choices

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        if self.account and amount:
            if amount > self.account.balance_due:
                raise ValidationError("Payment amount cannot be greater than the current balance due.")

        return amount
    
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            "project",
            "client",
            "title",
            "category",
            "amount",
            "expense_date",
            "vendor_name",
            "description",
            "receipt_file",
            "status",
            "notes",
        ]
        widgets = {
            "expense_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["project"].required = False
        self.fields["client"].required = False
        self.fields["project"].queryset = Project.objects.select_related("client").all().order_by("-created_at")
        self.fields["client"].queryset = Client.objects.all().order_by("legal_name")

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get("project")
        client = cleaned_data.get("client")

        if project and client and project.client_id != client.id:
            raise ValidationError("The selected project does not belong to the selected client.")

        return cleaned_data


class ExpenseFilterForm(forms.Form):
    search = forms.CharField(required=False)
    category = forms.ChoiceField(
        required=False,
        choices=[("", "All categories")] + list(ExpenseCategory.choices),
    )
    status = forms.ChoiceField(
        required=False,
        choices=[("", "All statuses")] + list(ExpenseStatus.choices),
    )
    project = forms.ModelChoiceField(
        required=False,
        queryset=Project.objects.all().order_by("-created_at"),
    )
    client = forms.ModelChoiceField(
        required=False,
        queryset=Client.objects.all().order_by("legal_name"),
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )