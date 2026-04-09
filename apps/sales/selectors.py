from django.db.models import Count, Prefetch, Q

from .models import Opportunity, OpportunityStage, OpportunityStatus


def get_stage_queryset():
    return OpportunityStage.objects.order_by("position", "name")


def get_opportunity_queryset():
    return Opportunity.objects.select_related(
        "client",
        "stage",
        "responsible",
        "created_by",
        "updated_by",
    ).order_by("-created_at")


def get_opportunity_detail_queryset():
    return get_opportunity_queryset().prefetch_related(
        Prefetch(
            "stage_history",
            queryset=(
                Opportunity.stage_history.rel.related_model.objects.select_related(
                    "from_stage",
                    "to_stage",
                    "changed_by",
                ).order_by("-moved_at", "-created_at")
            ),
        )
    )


def get_kanban_stage_queryset(*, responsible=None, client=None, include_closed=False):
    opportunity_filter = Q()
    count_filter = Q()

    if not include_closed:
        opportunity_filter &= Q(status=OpportunityStatus.OPEN)
        count_filter &= Q(opportunities__status=OpportunityStatus.OPEN)

    if responsible is not None:
        opportunity_filter &= Q(responsible=responsible)
        count_filter &= Q(opportunities__responsible=responsible)

    if client is not None:
        opportunity_filter &= Q(client=client)
        count_filter &= Q(opportunities__client=client)

    filtered_opportunities = get_opportunity_queryset().filter(opportunity_filter)

    return (
        get_stage_queryset()
        .filter(is_active=True)
        .prefetch_related(
            Prefetch(
                "opportunities",
                queryset=filtered_opportunities,
                to_attr="kanban_opportunities",
            )
        )
        .annotate(
            kanban_opportunity_count=Count(
                "opportunities",
                filter=count_filter,
                distinct=True,
            )
        )
    )