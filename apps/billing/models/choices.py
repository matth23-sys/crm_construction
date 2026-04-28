# -*- coding: utf-8 -*-

from django.db import models


class AccountReceivableStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PARTIALLY_PAID = "partially_paid", "Partially paid"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"


class PaymentMethod(models.TextChoices):
    CASH = "cash", "Cash"
    CHECK = "check", "Check"
    BANK_TRANSFER = "bank_transfer", "Bank transfer"
    CREDIT_CARD = "credit_card", "Credit card"
    DEBIT_CARD = "debit_card", "Debit card"
    ZELLE = "zelle", "Zelle"
    OTHER = "other", "Other"

class ExpenseCategory(models.TextChoices):
    MATERIALS = "materials", "Materials"
    LABOR = "labor", "Labor / Payroll"
    SUBCONTRACTOR = "subcontractor", "Subcontractor"
    EQUIPMENT = "equipment", "Equipment"
    FUEL = "fuel", "Fuel / Transportation"
    PERMITS = "permits", "Permits"
    TOOLS = "tools", "Tools"
    OFFICE = "office", "Office"
    OTHER = "other", "Other"


class ExpenseStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"