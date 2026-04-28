# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.views.generic import TemplateView 
from .models import Opportunity, OpportunityStage
from .forms import OpportunityForm, OpportunityStageMoveForm, OpportunityFilterForm
from .services import create_opportunity, move_opportunity_stage, build_project_seed_from_opportunity
from .selectors import get_opportunity_list, get_kanban_board, get_opportunity_detail




class OpportunityListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'sales.view_opportunity'
    template_name = 'sales/opportunity_list.html'
    context_object_name = 'opportunities'
    paginate_by = 25

    def get_queryset(self):
        qs = get_opportunity_list(user=self.request.user)
        form = OpportunityFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('client'):
                qs = qs.filter(client=form.cleaned_data['client'])
            if form.cleaned_data.get('responsible'):
                qs = qs.filter(responsible_id=form.cleaned_data['responsible'])
            if form.cleaned_data.get('search'):
                qs = qs.filter(
                    Q(title__icontains=form.cleaned_data['search']) |
                    Q(client__legal_name__icontains=form.cleaned_data['search'])
                )
            if not form.cleaned_data.get('include_closed'):
                qs = qs.filter(status='open')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = OpportunityFilterForm(self.request.GET)
        from apps.users.models import User
        context['filter_form'].fields['responsible'].choices = [('', '---------')] + [
            (u.id, u.get_full_name() or u.username) for u in User.objects.filter(is_active=True)
        ]
        return context


class OpportunityKanbanView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'sales.view_opportunity'
    template_name = 'sales/opportunity_kanban.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = get_kanban_board()   # El diccionario con etapas y oportunidades
        return context

class OpportunityCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'sales.add_opportunity'
    form_class = OpportunityForm
    template_name = 'sales/opportunity_form.html'

    def form_valid(self, form):
        # Usar el servicio en lugar de form.save()
        opportunity = create_opportunity(
            client=form.cleaned_data['client'],
            title=form.cleaned_data['title'],
            description=form.cleaned_data.get('description', ''),
            estimated_value=form.cleaned_data.get('estimated_value'),
            responsible=form.cleaned_data['responsible'],
            created_by=self.request.user,
        )
        return redirect('sales:detail', pk=opportunity.pk)
    
class OpportunityUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'sales.change_opportunity'
    model = Opportunity
    form_class = OpportunityForm
    template_name = 'sales/opportunity_form.html'

    def get_success_url(self):
        return reverse_lazy('sales:detail', kwargs={'pk': self.object.pk})


class OpportunityDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'sales.view_opportunity'
    model = Opportunity
    template_name = 'sales/opportunity_detail.html'
    context_object_name = 'opportunity'

    def get_object(self, queryset=None):
        # Usar el selector que ya hace select_related y prefetch_related
        return get_opportunity_detail(self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["move_form"] = OpportunityStageMoveForm(opportunity=self.object)

        has_related_project = hasattr(self.object, "project")
        context["has_related_project"] = has_related_project
        context["related_project"] = self.object.project if has_related_project else None

        return context


class OpportunityMoveStageView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "sales.move_opportunity"

    def post(self, request, pk):
        opportunity = get_object_or_404(Opportunity, pk=pk)
        form = OpportunityStageMoveForm(request.POST, opportunity=opportunity)

        if not form.is_valid():
            messages.error(request, f"No se pudo mover la oportunidad. Errores: {form.errors}")
            return redirect("sales:detail", pk=pk)

        try:
            move_opportunity_stage(
                opportunity=opportunity,
                to_stage=form.cleaned_data["to_stage"],
                changed_by=request.user,
                note=form.cleaned_data.get("note", ""),
            )
            messages.success(request, "La oportunidad fue movida correctamente.")
        except ValidationError as e:
            messages.error(request, str(e))

        return redirect("sales:detail", pk=pk)


from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from .models import Opportunity
from .services import build_project_seed_from_opportunity


def _make_json_safe(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, list):
        return [_make_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_make_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {key: _make_json_safe(val) for key, val in value.items()}
    return value


def _project_seed_to_session_dict(project_seed):
    if is_dataclass(project_seed):
        payload = asdict(project_seed)
    elif isinstance(project_seed, dict):
        payload = project_seed
    else:
        payload = {
            key: value
            for key, value in project_seed.__dict__.items()
            if not key.startswith("_")
        }

    return _make_json_safe(payload)


class OpportunityConvertToProjectView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "sales.convert_opportunity"

    def get(self, request, pk):
        messages.info(request, "La conversión debe ejecutarse desde el botón del detalle de la oportunidad.")
        return redirect("sales:detail", pk=pk)

    def post(self, request, pk):
        opportunity = get_object_or_404(
            Opportunity.objects.select_related("client", "responsible", "stage"),
            pk=pk,
        )

        if getattr(opportunity, "project", None):
            messages.info(request, "Esta oportunidad ya tiene un proyecto relacionado.")
            return redirect("projects:detail", pk=opportunity.project.pk)

        if not getattr(opportunity.stage, "is_won_stage", False):
            messages.error(request, "Solo las oportunidades ganadas pueden convertirse en proyecto.")
            return redirect("sales:detail", pk=pk)

        try:
            project_seed = build_project_seed_from_opportunity(opportunity)
            request.session["project_seed"] = _project_seed_to_session_dict(project_seed)
            request.session.modified = True
            messages.success(request, "Oportunidad convertida. Ahora puedes crear el proyecto.")
            return redirect("projects:create_from_opportunity")
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("sales:detail", pk=pk)