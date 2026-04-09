from __future__ import annotations

import uuid
from decimal import Decimal

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase
from django.utils import timezone

from apps.sales.models import OpportunityStatus, OpportunityStage
from apps.sales.services import (
    build_project_seed_from_opportunity,
    create_opportunity,
    move_opportunity_stage,
)
from apps.users.models import User


Client = apps.get_model("clients", "Client")


def _first_choice_value(field) -> str | None:
    if not field.choices:
        return None

    valid_choices = [choice[0] for choice in field.choices if choice[0] not in (None, "")]
    return valid_choices[0] if valid_choices else None


def build_minimal_client():
    """
    Creates a minimally valid Client instance by inspecting the real model fields.
    This avoids hard-coding too many assumptions from the clients module.
    """
    unique_token = uuid.uuid4().hex[:10]
    data = {}

    ignored_names = {
        "id",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "deactivated_at",
        "deactivated_by",
    }

    for field in Client._meta.fields:
        if field.auto_created or field.name in ignored_names:
            continue

        if field.default is not models.NOT_PROVIDED:
            continue

        if getattr(field, "null", False) or getattr(field, "blank", False):
            continue

        if field.name == "legal_name":
            data[field.name] = f"Acme Construction {unique_token}"
            continue

        if field.name == "commercial_name":
            data[field.name] = f"Acme {unique_token}"
            continue

        if field.name == "document_number":
            data[field.name] = unique_token
            continue

        if field.choices:
            choice_value = _first_choice_value(field)
            if choice_value is not None:
                data[field.name] = choice_value
                continue

        if isinstance(field, models.EmailField):
            data[field.name] = f"client-{unique_token}@example.com"
        elif isinstance(field, models.BooleanField):
            data[field.name] = True
        elif isinstance(field, models.IntegerField):
            data[field.name] = 1
        elif isinstance(field, models.DecimalField):
            data[field.name] = Decimal("0.00")
        elif isinstance(field, models.DateField):
            data[field.name] = timezone.localdate()
        else:
            data[field.name] = f"Value {field.name} {unique_token}"

    return Client.objects.create(**data)


class OpportunityServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sales-admin",
            email="sales-admin@example.com",
            password="StrongPass123!",
        )
        self.client_instance = build_minimal_client()

        self.lead_stage = OpportunityStage.objects.create(
            name="Lead",
            code="lead",
            position=10,
            is_default=True,
        )
        self.won_stage = OpportunityStage.objects.create(
            name="Won",
            code="won",
            position=50,
            is_won_stage=True,
        )

    def test_create_opportunity_registers_initial_stage_history(self):
        opportunity = create_opportunity(
            client=self.client_instance,
            title="Kitchen remodeling for north zone",
            created_by=self.user,
            responsible=self.user,
            estimated_value=Decimal("4500.00"),
        )

        self.assertEqual(opportunity.stage, self.lead_stage)
        self.assertEqual(opportunity.status, OpportunityStatus.OPEN)
        self.assertEqual(opportunity.stage_history.count(), 1)

        history_entry = opportunity.stage_history.first()
        self.assertIsNone(history_entry.from_stage)
        self.assertEqual(history_entry.to_stage, self.lead_stage)

    def test_move_opportunity_stage_updates_status_and_history(self):
        opportunity = create_opportunity(
            client=self.client_instance,
            title="Bathroom remodeling lead",
            created_by=self.user,
            responsible=self.user,
        )

        move_opportunity_stage(
            opportunity,
            to_stage=self.won_stage,
            changed_by=self.user,
            note="Client accepted the proposal.",
        )

        opportunity.refresh_from_db()

        self.assertEqual(opportunity.stage, self.won_stage)
        self.assertEqual(opportunity.status, OpportunityStatus.WON)
        self.assertIsNotNone(opportunity.closed_at)
        self.assertEqual(opportunity.stage_history.count(), 2)

    def test_build_project_seed_requires_won_opportunity(self):
        opportunity = create_opportunity(
            client=self.client_instance,
            title="Deck opportunity",
            created_by=self.user,
        )

        with self.assertRaises(ValidationError):
            build_project_seed_from_opportunity(opportunity)

    def test_build_project_seed_returns_payload_for_won_opportunity(self):
        opportunity = create_opportunity(
            client=self.client_instance,
            title="Full house remodeling",
            created_by=self.user,
            responsible=self.user,
            estimated_value=Decimal("12500.00"),
        )

        move_opportunity_stage(
            opportunity,
            to_stage=self.won_stage,
            changed_by=self.user,
            note="Closed and ready for project creation.",
        )

        opportunity.refresh_from_db()
        payload = build_project_seed_from_opportunity(opportunity)

        self.assertEqual(payload.client_id, str(self.client_instance.pk))
        self.assertEqual(payload.opportunity_id, str(opportunity.pk))
        self.assertEqual(payload.suggested_name, "Full house remodeling")
        self.assertEqual(payload.responsible_id, str(self.user.pk))
        self.assertEqual(payload.metadata["stage_code"], "won")