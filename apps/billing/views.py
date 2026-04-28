# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from apps.billing.forms import (
    AccountReceivableFilterForm,
    AccountReceivableForm,
    PaymentForm,
)
from apps.billing.models import AccountReceivable
from apps.billing.permissions import BillingPermissionRequiredMixin
from apps.billing.selectors import (
    get_account_receivable_detail,
    get_account_receivable_list,
    get_billing_summary,
    get_payments_for_account,
    get_pending_account_receivable_list,
)
from apps.billing.services import (
    cancel_account_receivable,
    create_account_receivable,
    register_payment,
    update_account_receivable,
)


class AccountReceivableListView(BillingPermissionRequiredMixin, ListView):
    template_name = "billing/list.html"
    context_object_name = "accounts"
    paginate_by = 20
    permission_required = "billing.view_accountreceivable"

    def get_queryset(self):
        self.filter_form = AccountReceivableFilterForm(self.request.GET or None)
        filters = {}

        if self.filter_form.is_valid():
            filters = self.filter_form.cleaned_data

        return get_account_receivable_list(filters=filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        context["summary"] = get_billing_summary()
        return context


class PendingAccountReceivableListView(BillingPermissionRequiredMixin, ListView):
    template_name = "billing/pending_list.html"
    context_object_name = "accounts"
    paginate_by = 20
    permission_required = "billing.view_pending_accounts"

    def get_queryset(self):
        self.filter_form = AccountReceivableFilterForm(self.request.GET or None)
        filters = {}

        if self.filter_form.is_valid():
            filters = self.filter_form.cleaned_data

        return get_pending_account_receivable_list(filters=filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        context["summary"] = get_billing_summary()
        return context


class AccountReceivableCreateView(BillingPermissionRequiredMixin, CreateView):
    template_name = "billing/form.html"
    form_class = AccountReceivableForm
    permission_required = "billing.add_accountreceivable"

    def form_valid(self, form):
        try:
            self.object = create_account_receivable(
                data=form.cleaned_data,
                user=self.request.user,
            )
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)

        messages.success(self.request, "Account receivable created successfully.")
        return redirect(self.object.get_absolute_url())


class AccountReceivableUpdateView(BillingPermissionRequiredMixin, UpdateView):
    template_name = "billing/form.html"
    form_class = AccountReceivableForm
    permission_required = "billing.change_accountreceivable"

    def get_queryset(self):
        return AccountReceivable.objects.select_related("client", "project")

    def form_valid(self, form):
        try:
            self.object = update_account_receivable(
                account=self.object,
                data=form.cleaned_data,
                user=self.request.user,
            )
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)

        messages.success(self.request, "Account receivable updated successfully.")
        return redirect(self.object.get_absolute_url())


class AccountReceivableDetailView(BillingPermissionRequiredMixin, DetailView):
    template_name = "billing/detail.html"
    context_object_name = "account"
    permission_required = "billing.view_accountreceivable"

    def get_object(self, queryset=None):
        return get_account_receivable_detail(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.object
        context["payments"] = get_payments_for_account(account)
        context["payment_form"] = PaymentForm(account=account)
        return context


class PaymentRegisterView(BillingPermissionRequiredMixin, View):
    permission_required = "billing.register_payment"

    def post(self, request, pk):
        account = get_account_receivable_detail(pk)
        form = PaymentForm(request.POST, request.FILES, account=account)

        if form.is_valid():
            try:
                register_payment(
                    account=account,
                    data=form.cleaned_data,
                    user=request.user,
                )
            except ValidationError as exc:
                form.add_error(None, exc)
            else:
                messages.success(request, "Payment registered successfully.")
                return redirect(account.get_absolute_url())

        payments = get_payments_for_account(account)
        return render(
            request,
            "billing/detail.html",
            {
                "account": account,
                "payments": payments,
                "payment_form": form,
            },
        )


class AccountReceivableCancelView(BillingPermissionRequiredMixin, View):
    permission_required = "billing.cancel_account_receivable"

    def post(self, request, pk):
        account = get_account_receivable_detail(pk)
        reason = request.POST.get("reason", "")

        try:
            cancel_account_receivable(
                account=account,
                user=request.user,
                reason=reason,
            )
        except ValidationError as exc:
            messages.error(request, exc.message if hasattr(exc, "message") else str(exc))
        else:
            messages.success(request, "Account receivable cancelled successfully.")

        return redirect(reverse("billing:detail", kwargs={"pk": pk}))