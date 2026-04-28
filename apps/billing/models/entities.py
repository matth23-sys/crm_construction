# -*- coding: utf-8 -*-
from apps.billing.models.choices import (
    AccountReceivableStatus,
    PaymentMethod,
    ExpenseCategory,
    ExpenseStatus,
)

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import FileExtensionValidator

from core.db.base import BaseModel
from apps.billing.models.choices import AccountReceivableStatus, PaymentMethod

def billing_receipt_upload_to(instance, filename):
    return f"billing/receipts/payments/{instance.account_id}/{filename}"

class AccountReceivable(BaseModel):
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.PROTECT,
        related_name="accounts_receivable",
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.PROTECT,
        related_name="accounts_receivable",
        blank=True,
        null=True,
    )

    title = models.CharField(max_length=180)
    invoice_number = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    balance_due = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    issued_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(blank=True, null=True)

    status = models.CharField(
        max_length=30,
        choices=AccountReceivableStatus.choices,
        default=AccountReceivableStatus.PENDING,
        db_index=True,
    )

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-issued_date", "-created_at"]
        verbose_name = "Account receivable"
        verbose_name_plural = "Accounts receivable"
        permissions = [
            ("register_payment", "Can register payment"),
            ("view_pending_accounts", "Can view pending accounts"),
            ("cancel_account_receivable", "Can cancel account receivable"),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(total_amount__gte=Decimal("0.01")),
                name="billing_account_total_amount_positive",
            ),
            models.CheckConstraint(
                check=models.Q(amount_paid__gte=Decimal("0.00")),
                name="billing_account_amount_paid_non_negative",
            ),
            models.CheckConstraint(
                check=models.Q(balance_due__gte=Decimal("0.00")),
                name="billing_account_balance_due_non_negative",
            ),
        ]
        

    def __str__(self):
        return f"{self.title} - {self.client}"

    def clean(self):
        errors = {}

        if self.project_id and self.client_id:
            project_client_id = getattr(self.project, "client_id", None)
            if project_client_id and project_client_id != self.client_id:
                errors["project"] = "The selected project does not belong to the selected client."

        if self.due_date and self.issued_date and self.due_date < self.issued_date:
            errors["due_date"] = "Due date cannot be earlier than issued date."

        if self.amount_paid and self.total_amount and self.amount_paid > self.total_amount:
            errors["amount_paid"] = "Amount paid cannot be greater than total amount."

        if errors:
            raise ValidationError(errors)

    @property
    def is_paid(self):
        return self.status == AccountReceivableStatus.PAID

    @property
    def is_cancelled(self):
        return self.status == AccountReceivableStatus.CANCELLED

    @property
    def is_overdue(self):
        if not self.due_date:
            return False
        return (
            self.due_date < timezone.localdate()
            and self.balance_due > Decimal("0.00")
            and self.status not in [
                AccountReceivableStatus.PAID,
                AccountReceivableStatus.CANCELLED,
            ]
        )

    def get_absolute_url(self):
        return reverse("billing:detail", kwargs={"pk": self.pk})


class Payment(BaseModel):
    account = models.ForeignKey(
        AccountReceivable,
        on_delete=models.PROTECT,
        related_name="payments",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    payment_date = models.DateField(default=timezone.localdate)
    method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
    )
    reference_number = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="payments_received",
        blank=True,
        null=True,
    )
    

    receipt_file = models.FileField(
    upload_to=billing_receipt_upload_to,
    blank=True,
    null=True,
    validators=[
        FileExtensionValidator(
            allowed_extensions=["pdf", "jpg", "jpeg", "png", "webp"]
        )
    ],
    help_text="Upload a receipt, proof of payment, or payment confirmation.",
    )

    class Meta:
        ordering = ["-payment_date", "-created_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gte=Decimal("0.01")),
                name="billing_payment_amount_positive",
            ),
        ]

    def __str__(self):
        return f"Payment {self.amount} - {self.account}"

    def clean(self):
        errors = {}

        if self.account_id:
            if self.account.status == AccountReceivableStatus.CANCELLED:
                errors["account"] = "Cannot register payments for a cancelled account."

            if self.account.status == AccountReceivableStatus.PAID:
                errors["account"] = "Cannot register payments for a paid account."

            if self.amount and self.account.balance_due is not None:
                if self.amount > self.account.balance_due:
                    errors["amount"] = "Payment amount cannot be greater than the current balance due."

        if errors:
            raise ValidationError(errors)
        

def expense_receipt_upload_to(instance, filename):
    project_id = instance.project_id or "general"
    return f"billing/receipts/expenses/{project_id}/{filename}"


class Expense(BaseModel):
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.PROTECT,
        related_name="expenses",
        blank=True,
        null=True,
    )
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.PROTECT,
        related_name="expenses",
        blank=True,
        null=True,
    )

    title = models.CharField(max_length=180)
    category = models.CharField(
        max_length=40,
        choices=ExpenseCategory.choices,
        default=ExpenseCategory.OTHER,
        db_index=True,
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    expense_date = models.DateField(default=timezone.localdate)

    vendor_name = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)

    receipt_file = models.FileField(
        upload_to=expense_receipt_upload_to,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf", "jpg", "jpeg", "png", "webp"]
            )
        ],
    )

    status = models.CharField(
        max_length=30,
        choices=ExpenseStatus.choices,
        default=ExpenseStatus.PAID,
        db_index=True,
    )

    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="expenses_paid",
        blank=True,
        null=True,
    )

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-expense_date", "-created_at"]
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        permissions = [
            ("mark_expense_paid", "Can mark expense as paid"),
            ("cancel_expense", "Can cancel expense"),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gte=Decimal("0.01")),
                name="billing_expense_amount_positive",
            ),
        ]

    def __str__(self):
        return f"{self.title} - {self.amount}"

    def clean(self):
        errors = {}

        if self.project_id and self.client_id:
            project_client_id = getattr(self.project, "client_id", None)
            if project_client_id and project_client_id != self.client_id:
                errors["project"] = "The selected project does not belong to the selected client."

        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse("billing:expense_detail", kwargs={"pk": self.pk})