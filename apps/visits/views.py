from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView
import logging
from django.core.management import call_command
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_GET


from .forms import (
    TechnicalVisitFilterForm,
    TechnicalVisitForm,
    VisitReminderLogFilterForm,
    VisitRescheduleForm,
)
from .models import TechnicalVisit
from .permissions import VisitsPermissionRequiredMixin
from .selectors import get_visit_detail, get_visit_list, get_visit_reminder_logs
from .services import create_technical_visit, reschedule_technical_visit, update_technical_visit

class TechnicalVisitObjectMixin:
    _visit = None
    def get_visit(self):
        if self._visit is None:
            self._visit = get_object_or_404(TechnicalVisit, pk=self.kwargs["pk"])
        return self._visit

class TechnicalVisitListView(LoginRequiredMixin, VisitsPermissionRequiredMixin, ListView):
    template_name = "visits/list.html"
    context_object_name = "visits"
    paginate_by = 20
    permission_required = "visits.view_technicalvisit"

    def get_queryset(self):
        self.filter_form = TechnicalVisitFilterForm(self.request.GET or None)
        filters = self.filter_form.cleaned_data if self.filter_form.is_valid() else {}
        return get_visit_list(filters=filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        context["now"] = timezone.now()
        return context

class TechnicalVisitCreateView(LoginRequiredMixin, VisitsPermissionRequiredMixin, FormView):
    template_name = "visits/form.html"
    form_class = TechnicalVisitForm
    permission_required = "visits.add_technicalvisit"

    def form_valid(self, form):
        visit = create_technical_visit(actor=self.request.user, **form.cleaned_data)
        messages.success(self.request, "Technical visit created successfully.")
        return redirect("visits:detail", pk=visit.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Schedule technical visit"
        context["submit_label"] = "Save visit"
        context["cancel_url"] = reverse("visits:list")
        return context

class TechnicalVisitUpdateView(LoginRequiredMixin, VisitsPermissionRequiredMixin, TechnicalVisitObjectMixin, FormView):
    template_name = "visits/form.html"
    form_class = TechnicalVisitForm
    permission_required = "visits.change_technicalvisit"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_visit()
        return kwargs

    def form_valid(self, form):
        visit = update_technical_visit(visit=self.get_visit(), actor=self.request.user, **form.cleaned_data)
        messages.success(self.request, "Technical visit updated successfully.")
        return redirect("visits:detail", pk=visit.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["visit"] = self.get_visit()
        context["page_title"] = "Edit technical visit"
        context["submit_label"] = "Update visit"
        context["cancel_url"] = reverse("visits:detail", kwargs={"pk": self.get_visit().pk})
        return context

class TechnicalVisitDetailView(LoginRequiredMixin, VisitsPermissionRequiredMixin, DetailView):
    template_name = "visits/detail.html"
    context_object_name = "visit"
    permission_required = "visits.view_technicalvisit"

    def get_object(self, queryset=None):
        return get_visit_detail(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit = self.object
        context["recent_logs"] = visit.reminder_logs.all()[:10]
        if self.request.user.has_perm("visits.reschedule_technicalvisit"):
            context["reschedule_form"] = VisitRescheduleForm(
                initial={"scheduled_for": timezone.localtime(visit.scheduled_for).strftime("%Y-%m-%dT%H:%M")}
            )
        return context

class TechnicalVisitRescheduleView(LoginRequiredMixin, VisitsPermissionRequiredMixin, TechnicalVisitObjectMixin, FormView):
    form_class = VisitRescheduleForm
    permission_required = "visits.reschedule_technicalvisit"
    template_name = "visits/form.html"

    def form_valid(self, form):
        visit = reschedule_technical_visit(
            visit=self.get_visit(),
            new_scheduled_for=form.cleaned_data["scheduled_for"],
            actor=self.request.user,
            reason=form.cleaned_data.get("reschedule_reason", ""),
        )
        messages.success(self.request, "Technical visit rescheduled successfully.")
        return redirect("visits:detail", pk=visit.pk)

    def form_invalid(self, form):
        visit = get_visit_detail(self.get_visit().pk)
        return self.render_to_response(
            self.get_context_data(
                form=form,
                visit=visit,
                page_title="Reschedule technical visit",
                submit_label="Reschedule visit",
                cancel_url=reverse("visits:detail", kwargs={"pk": visit.pk}),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit = kwargs.get("visit") or self.get_visit()
        context["visit"] = visit
        context["page_title"] = "Reschedule technical visit"
        context["submit_label"] = "Reschedule visit"
        context["cancel_url"] = reverse("visits:detail", kwargs={"pk": visit.pk})
        return context

class VisitReminderLogListView(LoginRequiredMixin, VisitsPermissionRequiredMixin, ListView):
    template_name = "visits/reminder_log_list.html"
    context_object_name = "logs"
    paginate_by = 30
    permission_required = "visits.view_visitreminderlog"

    def get_queryset(self):
        self.filter_form = VisitReminderLogFilterForm(self.request.GET or None)
        filters = self.filter_form.cleaned_data if self.filter_form.is_valid() else {}
        return get_visit_reminder_logs(filters=filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        return context
    

logger = logging.getLogger(__name__)


@require_GET
def run_visit_reminders_cron(request):
    configured_token = getattr(settings, "CRON_TOKEN", "")
    request_token = request.GET.get("token", "")

    if not configured_token or request_token != configured_token:
        return JsonResponse(
            {"error": "Token inválido o no configurado"},
            status=403,
        )

    target_date = request.GET.get("date")
    retry_failed = request.GET.get("retry_failed", "").lower() in {
        "1",
        "true",
        "yes",
    }

    command_options = {}

    if target_date:
        command_options["date"] = target_date

    if retry_failed:
        command_options["retry_failed"] = True

    try:
        call_command("send_visit_reminders", **command_options)

        return JsonResponse(
            {
                "status": "ok",
                "message": "Recordatorios procesados correctamente",
            }
        )

    except Exception as exc:
        logger.exception("Error running cron for visit reminders")

        return JsonResponse(
            {
                "status": "error",
                "message": "No se pudieron procesar los recordatorios.",
                "error": str(exc),
            },
            status=500,
        )