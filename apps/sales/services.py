from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from decimal import Decimal
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import (
    Opportunity,
    OpportunitySource,
    OpportunityStage,
    OpportunityStageHistory,
    OpportunityStatus,
)


DEFAULT_STAGE_BLUEPRINTS = (
    {
        "name": "Lead",
        "code": "lead",
        "description": "New business opportunity pending qualification.",
        "color": "#64748B",
        "position": 10,
        "is_default": True,
        "is_won_stage": False,
        "is_lost_stage": False,
        "is_active": True,
    },
    {
        "name": "Qualified",
        "code": "qualified",
        "description": "Opportunity validated and relevant for the business.",
        "color": "#2563EB",
        "position": 20,
        "is_default": False,
        "is_won_stage": False,
        "is_lost_stage": False,
        "is_active": True,
    },
    {
        "name": "Proposal",
        "code": "proposal",
        "description": "Commercial proposal sent to the client.",
        "color": "#7C3AED",
        "position": 30,
        "is_default": False,
        "is_won_stage": False,
        "is_lost_stage": False,
        "is_active": True,
    },
    {
        "name": "Negotiation",
        "code": "negotiation",
        "description": "Commercial negotiation in progress.",
        "color": "#EA580C",
        "position": 40,
        "is_default": False,
        "is_won_stage": False,
        "is_lost_stage": False,
        "is_active": True,
    },
    {
        "name": "Won",
        "code": "won",
        "description": "Opportunity closed successfully.",
        "color": "#16A34A",
        "position": 50,
        "is_default": False,
        "is_won_stage": True,
        "is_lost_stage": False,
        "is_active": True,
    },
    {
        "name": "Lost",
        "code": "lost",
        "description": "Opportunity discarded or lost.",
        "color": "#DC2626",
        "position": 60,
        "is_default": False,
        "is_won_stage": False,
        "is_lost_stage": True,
        "is_active": True,
    },
)


def bootstrap_default_stages() -> list[OpportunityStage]:
    """
    Creates or updates a practical default pipeline for local/admin usage.
    Safe to run multiple times.
    """
    created_stages = []

    with transaction.atomic():
        for blueprint in DEFAULT_STAGE_BLUEPRINTS:
            stage, _ = OpportunityStage.objects.update_or_create(
                code=blueprint["code"],
                defaults=blueprint,
            )
            created_stages.append(stage)

        OpportunityStage.objects.exclude(code="lead").update(is_default=False)
        OpportunityStage.objects.exclude(code="won").update(is_won_stage=False)
        OpportunityStage.objects.exclude(code="lost").update(is_lost_stage=False)

    return list(OpportunityStage.objects.order_by("position", "name"))


def get_default_stage() -> OpportunityStage:
    stage = OpportunityStage.objects.filter(
        is_default=True,
        is_active=True,
    ).first()

    if not stage:
        stage = OpportunityStage.objects.filter(
            is_active=True,
        ).order_by("position").first()

    if not stage:
        raise ValidationError("No active opportunity stage is configured.")

    return stage

def _create_stage_history_entry(
    *,
    opportunity: Opportunity,
    from_stage: OpportunityStage | None,
    to_stage: OpportunityStage,
    changed_by,
    note: str = "",
) -> OpportunityStageHistory:
    history_entry = OpportunityStageHistory(
        opportunity=opportunity,
        from_stage=from_stage,
        to_stage=to_stage,
        changed_by=changed_by,
        note=note or "",
        moved_at=timezone.now(),
        created_by=changed_by,
        updated_by=changed_by,
    )
    history_entry.full_clean()
    history_entry.save()
    return history_entry


@transaction.atomic
def create_opportunity(
    *,
    client,
    title: str,
    created_by,
    stage: OpportunityStage | None = None,
    responsible=None,
    description: str = "",
    estimated_value: Decimal | None = None,
    expected_close_date: date | None = None,
    source: str = OpportunitySource.OTHER,
    internal_notes: str = "",
) -> Opportunity:
    stage = stage or get_default_stage()
    opportunity = Opportunity(
        client=client,
        title=title.strip(),
        description=description.strip(),
        stage=stage,
        responsible=responsible,
        estimated_value=estimated_value if estimated_value is not None else Decimal("0.00"),
        expected_close_date=expected_close_date,
        source=source,
        internal_notes=internal_notes.strip(),
        created_by=created_by,
        updated_by=created_by,
    )
    opportunity.full_clean()
    opportunity.save()

    _create_stage_history_entry(
        opportunity=opportunity,
        from_stage=None,
        to_stage=stage,
        changed_by=created_by,
        note="Initial stage assigned.",
    )
    return opportunity


@transaction.atomic
def update_opportunity(
    opportunity: Opportunity,
    *,
    updated_by,
    **data: Any,
) -> Opportunity:
    if "stage" in data:
        raise ValidationError("Use move_opportunity_stage() to change the opportunity stage.")

    for field_name, value in data.items():
        setattr(opportunity, field_name, value)

    opportunity.updated_by = updated_by
    opportunity.full_clean()
    opportunity.save()
    return opportunity


@transaction.atomic
def move_opportunity_stage(
    opportunity: Opportunity,
    *,
    to_stage: OpportunityStage,
    changed_by,
    note: str = "",
) -> Opportunity:
    if not to_stage.is_active:
        raise ValidationError("You cannot move an opportunity to an inactive stage.")

    current_stage = opportunity.stage

    if current_stage.pk == to_stage.pk:
        raise ValidationError("The opportunity is already in the selected stage.")

    opportunity.stage = to_stage
    opportunity.updated_by = changed_by
    opportunity.full_clean()
    opportunity.save()

    _create_stage_history_entry(
        opportunity=opportunity,
        from_stage=current_stage,
        to_stage=to_stage,
        changed_by=changed_by,
        note=note,
    )
    return opportunity


@dataclass(frozen=True)
class ProjectSeedPayload:
    client_id: str
    opportunity_id: str
    suggested_name: str
    description: str
    responsible_id: str | None
    estimated_value: Decimal
    expected_close_date: date | None
    internal_notes: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if payload["estimated_value"] is not None:
            payload["estimated_value"] = str(payload["estimated_value"])
        if payload["expected_close_date"] is not None:
            payload["expected_close_date"] = payload["expected_close_date"].isoformat()
        return payload


def build_project_seed_from_opportunity(opportunity: Opportunity) -> ProjectSeedPayload:
    if opportunity.status != OpportunityStatus.WON:
        raise ValidationError("Only won opportunities can be converted into a project seed.")

    if not opportunity.stage.is_won_stage:
        raise ValidationError("The current opportunity stage is not configured as a won stage.")

    client_display_name = getattr(opportunity.client, "display_name", None)
    if not client_display_name:
        client_display_name = getattr(opportunity.client, "commercial_name", None) or getattr(
            opportunity.client, "legal_name", str(opportunity.client_id)
        )

    return ProjectSeedPayload(
        client_id=str(opportunity.client_id),
        opportunity_id=str(opportunity.pk),
        suggested_name=opportunity.title.strip(),
        description=opportunity.description,
        responsible_id=str(opportunity.responsible_id) if opportunity.responsible_id else None,
        estimated_value=opportunity.estimated_value,
        expected_close_date=opportunity.expected_close_date,
        internal_notes=opportunity.internal_notes,
        metadata={
            "client_display_name": client_display_name,
            "source": opportunity.source,
            "status": opportunity.status,
            "stage_code": opportunity.stage.code,
            "stage_name": opportunity.stage.name,
            "closed_at": opportunity.closed_at.isoformat() if opportunity.closed_at else None,
        },
    )