from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.sales.models import OpportunityStage


class OpportunityStageModelTests(TestCase):
    def test_only_one_default_stage_is_allowed(self):
        OpportunityStage.objects.create(
            name="Lead",
            code="lead",
            position=10,
            is_default=True,
        )

        second_default = OpportunityStage(
            name="Qualified",
            code="qualified",
            position=20,
            is_default=True,
        )

        with self.assertRaises(ValidationError):
            second_default.full_clean()

    def test_only_one_won_stage_is_allowed(self):
        OpportunityStage.objects.create(
            name="Won",
            code="won",
            position=50,
            is_won_stage=True,
        )

        second_won = OpportunityStage(
            name="Closed Won",
            code="closed-won",
            position=60,
            is_won_stage=True,
        )

        with self.assertRaises(ValidationError):
            second_won.full_clean()

    def test_stage_cannot_be_won_and_lost_at_the_same_time(self):
        stage = OpportunityStage(
            name="Invalid terminal",
            code="invalid-terminal",
            position=90,
            is_won_stage=True,
            is_lost_stage=True,
        )

        with self.assertRaises(ValidationError):
            stage.full_clean()