# -*- coding: utf-8 -*-

from django.db.models import Count, Q, Sum
from django.utils import timezone
from apps.billing.models import AccountReceivable, Payment, Expense
from apps.billing.models import AccountReceivable, Payment
from apps.billing.models.choices import AccountReceivableStatus


def get_account_receivable_base_queryset():
    return (
        AccountReceivable.objects.select_related(
            "client",
            "project",
            "created_by",
            "updated_by",
        )
        .annotate(payments_count=Count("payments"))
    )


def get_account_receivable_list(filters=None):
    filters = filters or {}
    qs = get_account_receivable_base_queryset()

    search = filters.get("search")
    status = filters.get("status")
    client = filters.get("client")
    project = filters.get("project")
    due_from = filters.get("due_from")
    due_to = filters.get("due_to")
    only_overdue = filters.get("only_overdue")

    if search:
        qs = qs.filter(
            Q(title__icontains=search)
            | Q(invoice_number__icontains=search)
            | Q(description__icontains=search)
            | Q(client__legal_name__icontains=search)
            | Q(client__commercial_name__icontains=search)
            | Q(client__email__icontains=search)
            | Q(client__phone__icontains=search)
            | Q(project__name__icontains=search)
        )

    if status:
        qs = qs.filter(status=status)

    if client:
        qs = qs.filter(client=client)

    if project:
        qs = qs.filter(project=project)

    if due_from:
        qs = qs.filter(due_date__gte=due_from)

    if due_to:
        qs = qs.filter(due_date__lte=due_to)

    if only_overdue:
        qs = qs.filter(
            due_date__lt=timezone.localdate(),
            balance_due__gt=0,
        ).exclude(
            status__in=[
                AccountReceivableStatus.PAID,
                AccountReceivableStatus.CANCELLED,
            ]
        )

    return qs


def get_pending_account_receivable_list(filters=None):
    filters = filters or {}
    filters["status"] = ""
    qs = get_account_receivable_list(filters=filters)
    return qs.filter(
        status__in=[
            AccountReceivableStatus.PENDING,
            AccountReceivableStatus.PARTIALLY_PAID,
        ],
        balance_due__gt=0,
    )


def get_account_receivable_detail(pk):
    return (
        get_account_receivable_base_queryset()
        .prefetch_related("payments")
        .get(pk=pk)
    )


def get_payments_for_account(account):
    return (
        Payment.objects.select_related(
            "account",
            "received_by",
            "created_by",
            "updated_by",
        )
        .filter(account=account)
        .order_by("-payment_date", "-created_at")
    )


def get_billing_summary():
    qs = AccountReceivable.objects.all()

    total_pending = qs.exclude(
        status__in=[
            AccountReceivableStatus.PAID,
            AccountReceivableStatus.CANCELLED,
        ]
    ).aggregate(total=Sum("balance_due"))["total"]

    total_paid = qs.aggregate(total=Sum("amount_paid"))["total"]

    overdue_count = qs.filter(
        due_date__lt=timezone.localdate(),
        balance_due__gt=0,
    ).exclude(
        status__in=[
            AccountReceivableStatus.PAID,
            AccountReceivableStatus.CANCELLED,
        ]
    ).count()

    return {
        "total_pending": total_pending or 0,
        "total_paid": total_paid or 0,
        "overdue_count": overdue_count,
    }

def get_expense_base_queryset():
    return Expense.objects.select_related(
        "project",
        "client",
        "paid_by",
        "created_by",
        "updated_by",
    )


def get_expense_list(filters=None):
    filters = filters or {}
    qs = get_expense_base_queryset()

    search = filters.get("search")
    category = filters.get("category")
    status = filters.get("status")
    project = filters.get("project")
    client = filters.get("client")
    date_from = filters.get("date_from")
    date_to = filters.get("date_to")

    if search:
        qs = qs.filter(
            Q(title__icontains=search)
            | Q(vendor_name__icontains=search)
            | Q(description__icontains=search)
            | Q(project__name__icontains=search)
            | Q(client__legal_name__icontains=search)
            | Q(client__commercial_name__icontains=search)
        )

    if category:
        qs = qs.filter(category=category)

    if status:
        qs = qs.filter(status=status)

    if project:
        qs = qs.filter(project=project)

    if client:
        qs = qs.filter(client=client)

    if date_from:
        qs = qs.filter(expense_date__gte=date_from)

    if date_to:
        qs = qs.filter(expense_date__lte=date_to)

    return qs


def get_expense_detail(pk):
    return get_expense_base_queryset().get(pk=pk)