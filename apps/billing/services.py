# -*- coding: utf-8 -*-

from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from apps.billing.models import AccountReceivable, Payment, Expense
from apps.billing.models.choices import AccountReceivableStatus, ExpenseStatus
from apps.billing.models import AccountReceivable, Payment
from apps.billing.models.choices import AccountReceivableStatus


MONEY_QUANT = Decimal("0.01")


def normalize_money(value):
    if value is None:
        return Decimal("0.00")
    return Decimal(value).quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)


def set_user_tracking(instance, user, created=False):
    if user and getattr(user, "is_authenticated", False):
        if created and hasattr(instance, "created_by") and not instance.created_by_id:
            instance.created_by = user
        if hasattr(instance, "updated_by"):
            instance.updated_by = user


@transaction.atomic
def recalculate_account_receivable(account):
    account = AccountReceivable.objects.select_for_update().get(pk=account.pk)

    total_paid = (
        account.payments.aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )

    total_paid = normalize_money(total_paid)
    total_amount = normalize_money(account.total_amount)

    if total_paid > total_amount:
        raise ValidationError("Payments cannot be greater than account total amount.")

    balance_due = normalize_money(total_amount - total_paid)

    account.amount_paid = total_paid
    account.balance_due = balance_due

    if account.status != AccountReceivableStatus.CANCELLED:
        if balance_due == Decimal("0.00"):
            account.status = AccountReceivableStatus.PAID
        elif total_paid > Decimal("0.00"):
            account.status = AccountReceivableStatus.PARTIALLY_PAID
        else:
            account.status = AccountReceivableStatus.PENDING

    account.full_clean()
    account.save(
        update_fields=[
            "amount_paid",
            "balance_due",
            "status",
            "updated_at",
        ]
    )

    return account


@transaction.atomic
def create_account_receivable(*, data, user=None):
    account = AccountReceivable(**data)
    account.amount_paid = Decimal("0.00")
    account.balance_due = normalize_money(account.total_amount)
    account.status = AccountReceivableStatus.PENDING

    set_user_tracking(account, user, created=True)

    account.full_clean()
    account.save()

    return account


@transaction.atomic
def update_account_receivable(*, account, data, user=None):
    account = AccountReceivable.objects.select_for_update().get(pk=account.pk)

    protected_fields = {"amount_paid", "balance_due", "status"}
    for field, value in data.items():
        if field not in protected_fields:
            setattr(account, field, value)

    if normalize_money(account.total_amount) < normalize_money(account.amount_paid):
        raise ValidationError(
            "Total amount cannot be lower than the amount already paid."
        )

    account.balance_due = normalize_money(account.total_amount - account.amount_paid)

    if account.status != AccountReceivableStatus.CANCELLED:
        if account.balance_due == Decimal("0.00"):
            account.status = AccountReceivableStatus.PAID
        elif account.amount_paid > Decimal("0.00"):
            account.status = AccountReceivableStatus.PARTIALLY_PAID
        else:
            account.status = AccountReceivableStatus.PENDING

    set_user_tracking(account, user)

    account.full_clean()
    account.save()

    return account


@transaction.atomic
def register_payment(*, account, data, user=None):
    locked_account = AccountReceivable.objects.select_for_update().get(pk=account.pk)

    if locked_account.status == AccountReceivableStatus.CANCELLED:
        raise ValidationError("Cannot register payments for a cancelled account.")

    if locked_account.status == AccountReceivableStatus.PAID:
        raise ValidationError("Cannot register payments for a paid account.")

    amount = normalize_money(data.get("amount"))

    if amount <= Decimal("0.00"):
        raise ValidationError("Payment amount must be greater than zero.")

    if amount > normalize_money(locked_account.balance_due):
        raise ValidationError("Payment amount cannot be greater than the current balance due.")

    payment = Payment(
        account=locked_account,
        amount=amount,
        payment_date=data.get("payment_date"),
        method=data.get("method"),
        reference_number=data.get("reference_number", ""),
        receipt_file=data.get("receipt_file"),
        notes=data.get("notes", ""),
        received_by=user if user and getattr(user, "is_authenticated", False) else None,
    )

    set_user_tracking(payment, user, created=True)

    payment.full_clean()
    payment.save()

    recalculate_account_receivable(locked_account)

    return payment


@transaction.atomic
def cancel_account_receivable(*, account, user=None, reason=""):
    account = AccountReceivable.objects.select_for_update().get(pk=account.pk)

    if account.status == AccountReceivableStatus.PAID:
        raise ValidationError("A paid account cannot be cancelled.")

    account.status = AccountReceivableStatus.CANCELLED

    if reason:
        existing_notes = account.notes or ""
        account.notes = f"{existing_notes}\n\nCancellation reason: {reason}".strip()

    set_user_tracking(account, user)

    account.full_clean()
    account.save()

    return account

@transaction.atomic
def create_expense(*, data, user=None):
    expense = Expense(**data)

    if user and getattr(user, "is_authenticated", False):
        expense.paid_by = user if expense.status == ExpenseStatus.PAID else None

    set_user_tracking(expense, user, created=True)

    expense.full_clean()
    expense.save()

    return expense


@transaction.atomic
def update_expense(*, expense, data, user=None):
    expense = Expense.objects.select_for_update().get(pk=expense.pk)

    for field, value in data.items():
        setattr(expense, field, value)

    if user and getattr(user, "is_authenticated", False):
        if expense.status == ExpenseStatus.PAID and not expense.paid_by_id:
            expense.paid_by = user

    set_user_tracking(expense, user)

    expense.full_clean()
    expense.save()

    return expense


@transaction.atomic
def mark_expense_paid(*, expense, user=None):
    expense = Expense.objects.select_for_update().get(pk=expense.pk)

    if expense.status == ExpenseStatus.CANCELLED:
        raise ValidationError("A cancelled expense cannot be marked as paid.")

    expense.status = ExpenseStatus.PAID

    if user and getattr(user, "is_authenticated", False):
        expense.paid_by = user

    set_user_tracking(expense, user)

    expense.full_clean()
    expense.save()

    return expense


@transaction.atomic
def cancel_expense(*, expense, user=None, reason=""):
    expense = Expense.objects.select_for_update().get(pk=expense.pk)

    expense.status = ExpenseStatus.CANCELLED

    if reason:
        existing_notes = expense.notes or ""
        expense.notes = f"{existing_notes}\n\nCancellation reason: {reason}".strip()

    set_user_tracking(expense, user)

    expense.full_clean()
    expense.save()

    return expense