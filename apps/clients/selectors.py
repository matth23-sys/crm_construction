from django.db.models import Count, Max, Prefetch, Q

from .models import Client, ClientInteraction


def get_clients_queryset(*, search=None, status=None, client_type=None):
    queryset = (
        Client.objects.select_related("deactivated_by")
        .annotate(
            interactions_count=Count("interactions", distinct=True),
            last_interaction_at=Max("interactions__occurred_at"),
        )
        .order_by("legal_name", "commercial_name")
    )

    if search:
        search = search.strip()
        queryset = queryset.filter(
            Q(legal_name__icontains=search)
            | Q(commercial_name__icontains=search)
            | Q(document_number__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
            | Q(alternate_phone__icontains=search)
        )

    if status:
        queryset = queryset.filter(status=status)

    if client_type:
        queryset = queryset.filter(client_type=client_type)

    return queryset


def get_client_detail_queryset():
    interactions_queryset = ClientInteraction.objects.select_related(
        "registered_by",
        "client",
    ).order_by("-occurred_at", "-created_at")

    return Client.objects.select_related("deactivated_by").prefetch_related(
        Prefetch("interactions", queryset=interactions_queryset)
    )