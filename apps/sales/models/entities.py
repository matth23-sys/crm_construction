from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from core.db.base import BaseModel

from .choices import OpportunitySource, OpportunityStatus


class OpportunityStage(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=7,
        default="#1E293B",
        help_text="Hex color used by the kanban UI.",
    )
    position = models.PositiveSmallIntegerField(default=10, db_index=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    is_won_stage = models.BooleanField(default=False)
    is_lost_stage = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Opportunity stage"
        verbose_name_plural = "Opportunity stages"
        ordering = ("position", "name")

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        super().clean()

        if self.name and not self.code:
            self.code = slugify(self.name)

        if self.color and (not self.color.startswith("#") or len(self.color) != 7):
            raise ValidationError({"color": "Color must be a valid 7-character hex value, for example #1E293B."})

        if self.is_won_stage and self.is_lost_stage:
            raise ValidationError("A stage cannot be marked as won and lost at the same time.")

        if self.is_default and (self.is_won_stage or self.is_lost_stage):
            raise ValidationError("The default stage cannot be a terminal won or lost stage.")

        queryset = self.__class__.objects.all()
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        if self.is_default and queryset.filter(is_default=True).exists():
            raise ValidationError({"is_default": "There can only be one default opportunity stage."})

        if self.is_won_stage and queryset.filter(is_won_stage=True).exists():
            raise ValidationError({"is_won_stage": "There can only be one won opportunity stage."})

        if self.is_lost_stage and queryset.filter(is_lost_stage=True).exists():
            raise ValidationError({"is_lost_stage": "There can only be one lost opportunity stage."})

    def save(self, *args, **kwargs):
        if self.name and not self.code:
            self.code = slugify(self.name)
        return super().save(*args, **kwargs)


class Opportunity(BaseModel):
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.PROTECT,
        related_name="opportunities",
    )
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    stage = models.ForeignKey(
        "sales.OpportunityStage",
        on_delete=models.PROTECT,
        related_name="opportunities",
    )
    status = models.CharField(
        max_length=20,
        choices=OpportunityStatus.choices,
        default=OpportunityStatus.OPEN,
        editable=False,
        db_index=True,
    )
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales_opportunities",
    )
    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    expected_close_date = models.DateField(null=True, blank=True)
    source = models.CharField(
        max_length=30,
        choices=OpportunitySource.choices,
        default=OpportunitySource.OTHER,
        blank=True,
    )
    loss_reason = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    converted_to_project_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Opportunity"
        verbose_name_plural = "Opportunities"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status", "stage"]),
            models.Index(fields=["client", "status"]),
            models.Index(fields=["responsible", "status"]),
        ]
        permissions = [
            ("move_opportunity", "Can move opportunity between stages"),
            ("convert_opportunity", "Can build project seed from won opportunity"),
        ]

    def __str__(self) -> str:
        return self.title

    @property
    def is_closed(self) -> bool:
        return self.status in {OpportunityStatus.WON, OpportunityStatus.LOST}

    def sync_status_with_stage(self) -> None:
        if not self.stage_id:
            return

        if self.stage.is_won_stage:
            self.status = OpportunityStatus.WON
            if not self.closed_at:
                self.closed_at = timezone.now()
            return

        if self.stage.is_lost_stage:
            self.status = OpportunityStatus.LOST
            if not self.closed_at:
                self.closed_at = timezone.now()
            return

        self.status = OpportunityStatus.OPEN
        self.closed_at = None

    def clean(self) -> None:
        super().clean()

        if self.stage_id:
            self.sync_status_with_stage()

        if self.converted_to_project_at and self.status != OpportunityStatus.WON:
            raise ValidationError(
                {"converted_to_project_at": "Only won opportunities can be marked as converted to project."}
            )

    def save(self, *args, **kwargs):
        if self.stage_id:
            self.sync_status_with_stage()
        return super().save(*args, **kwargs)


class OpportunityStageHistory(BaseModel):
    opportunity = models.ForeignKey(
        "sales.Opportunity",
        on_delete=models.CASCADE,
        related_name="stage_history",
    )
    from_stage = models.ForeignKey(
        "sales.OpportunityStage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="history_entries_from",
    )
    to_stage = models.ForeignKey(
        "sales.OpportunityStage",
        on_delete=models.PROTECT,
        related_name="history_entries_to",
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="changed_opportunity_stages",
    )
    note = models.TextField(blank=True)
    moved_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        verbose_name = "Opportunity stage history"
        verbose_name_plural = "Opportunity stage history"
        ordering = ("-moved_at", "-created_at")
        get_latest_by = "moved_at"

    def __str__(self) -> str:
        return f"{self.opportunity} :: {self.from_stage} -> {self.to_stage}"

    def clean(self) -> None:
        super().clean()

        if self.from_stage_id and self.from_stage_id == self.to_stage_id:
            raise ValidationError({"to_stage": "Origin and destination stages cannot be the same."})