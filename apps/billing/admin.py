# -*- coding: utf-8 -*-

from django.contrib import admin
from apps.billing.models import AccountReceivable, Payment, Expense
from apps.billing.models import AccountReceivable, Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = (
        "amount",
        "payment_date",
        "method",
        "reference_number",
        "received_by",
        "created_at",
    )
    readonly_fields = ("created_at",)
    autocomplete_fields = ("received_by",)


@admin.register(AccountReceivable)
class AccountReceivableAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "project",
        "total_amount",
        "amount_paid",
        "balance_due",
        "status",
        "issued_date",
        "due_date",
    )
    list_filter = ("status", "issued_date", "due_date")
    search_fields = (
        "title",
        "invoice_number",
        "client__legal_name",
        "client__commercial_name",
        "project__name",
    )
    autocomplete_fields = ("client", "project", "created_by", "updated_by")
    readonly_fields = ("amount_paid", "balance_due", "created_at", "updated_at")
    inlines = [PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "amount",
        "payment_date",
        "method",
        "reference_number",
        "received_by",
    )
    list_filter = ("method", "payment_date")
    search_fields = (
        "account__title",
        "account__invoice_number",
        "reference_number",
        "notes",
    )
    autocomplete_fields = ("account", "received_by", "created_by", "updated_by")
    readonly_fields = ("created_at", "updated_at")

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "amount",
        "expense_date",
        "project",
        "client",
        "vendor_name",
        "status",
        "paid_by",
    )
    list_filter = ("category", "status", "expense_date")
    search_fields = (
        "title",
        "vendor_name",
        "description",
        "project__name",
        "client__legal_name",
        "client__commercial_name",
    )
    autocomplete_fields = (
        "project",
        "client",
        "paid_by",
        "created_by",
        "updated_by",
    )
    readonly_fields = ("created_at", "updated_at")