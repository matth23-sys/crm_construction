from django.db.models import Q
from .models import TechnicalVisit, VisitReminderLog

def get_visit_list(filters=None):
    queryset = TechnicalVisit.objects.select_related("client", "project", "responsible")
    if filters:
        if filters.get("search"):
            queryset = queryset.filter(
                Q(title__icontains=filters["search"]) |
                Q(client__legal_name__icontains=filters["search"]) |
                Q(client__commercial_name__icontains=filters["search"])
            )
        if filters.get("status"):
            queryset = queryset.filter(status=filters["status"])
        if filters.get("responsible"):
            queryset = queryset.filter(responsible=filters["responsible"])
        if filters.get("from_date"):
            queryset = queryset.filter(scheduled_for__date__gte=filters["from_date"])
        if filters.get("to_date"):
            queryset = queryset.filter(scheduled_for__date__lte=filters["to_date"])
    return queryset.order_by("-scheduled_for")

def get_visit_detail(pk):
    return TechnicalVisit.objects.select_related("client", "project", "responsible").get(pk=pk)

def get_visit_reminder_logs(filters=None):
    queryset = VisitReminderLog.objects.select_related("visit")
    if filters:
        if filters.get("status"):
            queryset = queryset.filter(status=filters["status"])
        if filters.get("reminder_type"):
            queryset = queryset.filter(reminder_type=filters["reminder_type"])
        if filters.get("visit_title"):
            queryset = queryset.filter(visit__title__icontains=filters["visit_title"])
    return queryset.order_by("-created_at")