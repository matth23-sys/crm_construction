from django.urls import path
from . import views
from .views import run_visit_reminders_cron

app_name = "visits"

urlpatterns = [
    path("", views.TechnicalVisitListView.as_view(), name="list"),
    path("create/", views.TechnicalVisitCreateView.as_view(), name="create"),
    path("<int:pk>/", views.TechnicalVisitDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.TechnicalVisitUpdateView.as_view(), name="edit"),
    path("<int:pk>/reschedule/", views.TechnicalVisitRescheduleView.as_view(), name="reschedule"),
    path("reminder-logs/", views.VisitReminderLogListView.as_view(), name="reminder_logs"),
    path('cron/visit-reminders/', run_visit_reminders_cron, name='cron_visit_reminders'),
]