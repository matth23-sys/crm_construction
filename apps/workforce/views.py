from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, TemplateView

from .forms import (
    FieldNoteForm,
    WorkforceMilestoneUpdateForm,
    WorkforceProjectFilterForm,
)
from .permissions import AssignedProjectAccessMixin
from .selectors import get_assigned_project_detail, get_my_assigned_projects
from .services import apply_worker_milestone_action, create_field_note


class MyProjectsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "workforce/list.html"
    context_object_name = "projects"
    paginate_by = 20
    permission_required = "workforce.view_assigned_projects"

    def get_filter_form(self):
        return WorkforceProjectFilterForm(self.request.GET or None)

    def get_queryset(self):
        self.filter_form = self.get_filter_form()
        filters = {}

        if self.filter_form.is_valid():
            filters = self.filter_form.cleaned_data

        return get_my_assigned_projects(
            user=self.request.user,
            filters=filters,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = getattr(self, "filter_form", self.get_filter_form())
        return context


class WorkforceProjectDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    AssignedProjectAccessMixin,
    TemplateView,
):
    template_name = "workforce/detail.html"
    permission_required = "workforce.view_assigned_projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        detail = get_assigned_project_detail(
            user=self.request.user,
            project_id=self.assigned_project.pk,
        )

        context.update(detail)
        context["field_note_form"] = FieldNoteForm()
        context["milestone_form"] = WorkforceMilestoneUpdateForm(
            project=detail["project"]
        )
        return context


class WorkforceFieldNoteCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    AssignedProjectAccessMixin,
    View,
):
    permission_required = "workforce.submit_field_note"

    def post(self, request, *args, **kwargs):
        form = FieldNoteForm(request.POST)

        if form.is_valid():
            create_field_note(
                project=self.assigned_project,
                author=request.user,
                body=form.cleaned_data["body"],
            )
            messages.success(request, "Field note saved successfully.")
            return redirect("workforce:detail", pk=self.assigned_project.pk)

        detail = get_assigned_project_detail(
            user=request.user,
            project_id=self.assigned_project.pk,
        )

        return render(
            request,
            "workforce/detail.html",
            {
                **detail,
                "field_note_form": form,
                "milestone_form": WorkforceMilestoneUpdateForm(
                    project=self.assigned_project
                ),
            },
            status=400,
        )


class WorkforceMilestoneUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    AssignedProjectAccessMixin,
    View,
):
    permission_required = "workforce.update_project_milestone"

    def post(self, request, *args, **kwargs):
        form = WorkforceMilestoneUpdateForm(
            request.POST,
            project=self.assigned_project,
        )

        if form.is_valid():
            try:
                apply_worker_milestone_action(
                    project=self.assigned_project,
                    user=request.user,
                    action=form.cleaned_data["action"],
                )
            except ValidationError as exc:
                form.add_error("action", exc.message)
            else:
                messages.success(request, "Milestone updated successfully.")
                return redirect("workforce:detail", pk=self.assigned_project.pk)

        detail = get_assigned_project_detail(
            user=request.user,
            project_id=self.assigned_project.pk,
        )

        return render(
            request,
            "workforce/detail.html",
            {
                **detail,
                "field_note_form": FieldNoteForm(),
                "milestone_form": form,
            },
            status=400,
        )