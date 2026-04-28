from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ProjectAssignmentForm, ProjectFilterForm, ProjectForm, ProjectNoteForm
from .models import Project, ProjectAssignment
from .permissions import (
    ADD_PROJECT_NOTE_PERMISSION,
    ADD_PROJECT_PERMISSION,
    CHANGE_PROJECT_PERMISSION,
    CREATE_FROM_OPPORTUNITY_PERMISSION,
    MANAGE_ASSIGNMENTS_PERMISSION,
    VIEW_PROJECT_PERMISSION,
    ProjectPermissionRequiredMixin,
)
from .selectors import get_project_detail, get_project_list
from .services import (
    add_project_note,
    assign_user_to_project,
    create_project,
    deactivate_project_assignment,
    update_project,
)


PROJECT_SEED_SESSION_KEYS = (
    "project_seed",
    "project_seed_from_opportunity",
    "opportunity_project_seed",
)


def _extract_project_seed(session):
    for key in PROJECT_SEED_SESSION_KEYS:
        if key in session:
            return key, session.get(key)
    return None, None


def _build_initial_from_seed(seed: dict) -> dict:
    return {
        "name": seed.get("project_name") or seed.get("name") or seed.get("title") or "",
        "description": seed.get("description") or seed.get("notes") or "",
        "location": seed.get("location") or seed.get("address") or "",
        "client": seed.get("client_id") or seed.get("client"),
        "opportunity": seed.get("opportunity_id") or seed.get("opportunity"),
        "responsible": seed.get("responsible_id") or seed.get("responsible"),
        "contract_amount": seed.get("contract_amount") or seed.get("estimated_value"),
    }


class ProjectListView(ProjectPermissionRequiredMixin, ListView):
    template_name = "projects/list.html"
    context_object_name = "projects"
    paginate_by = 20
    permission_required = VIEW_PROJECT_PERMISSION

    def get_filter_form(self):
        return ProjectFilterForm(self.request.GET or None)

    def get_queryset(self):
        self.filter_form = self.get_filter_form()
        filters = self.filter_form.cleaned_data if self.filter_form.is_valid() else {}
        return get_project_list(filters=filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = getattr(self, "filter_form", self.get_filter_form())
        return context


class ProjectCreateView(ProjectPermissionRequiredMixin, CreateView):
    template_name = "projects/form.html"
    form_class = ProjectForm
    permission_required = ADD_PROJECT_PERMISSION

    def form_valid(self, form):
        self.object = create_project(
            data=form.cleaned_data,
            created_by=self.request.user,
        )
        messages.success(self.request, "Project created successfully.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("projects:detail", kwargs={"pk": self.object.pk})


class ProjectCreateFromOpportunityView(ProjectPermissionRequiredMixin, CreateView):
    template_name = "projects/form.html"
    form_class = ProjectForm
    permission_required = (ADD_PROJECT_PERMISSION,)

    def dispatch(self, request, *args, **kwargs):
        self.seed_key, self.seed = _extract_project_seed(request.session)
        if not self.seed:
            messages.warning(
                request,
                "No conversion seed was found in session. Start the conversion from the opportunity detail."
            )
            return redirect("sales:list")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial.update(_build_initial_from_seed(self.seed))
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["from_opportunity"] = True
        context["seed"] = self.seed
        return context

    def form_valid(self, form):
        self.object = create_project(
            data=form.cleaned_data,
            created_by=self.request.user,
        )

        if self.seed_key and self.seed_key in self.request.session:
            del self.request.session[self.seed_key]
            self.request.session.modified = True

        messages.success(self.request, "Project created from opportunity successfully.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("projects:detail", kwargs={"pk": self.object.pk})


class ProjectDetailView(ProjectPermissionRequiredMixin, DetailView):
    template_name = "projects/detail.html"
    context_object_name = "project"
    permission_required = VIEW_PROJECT_PERMISSION

    def get_object(self, queryset=None):
        return get_project_detail(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        context["assignments"] = getattr(project, "prefetched_active_assignments", [])
        context["notes"] = getattr(project, "prefetched_notes", [])
        context["can_manage_assignments"] = self.request.user.has_perm(MANAGE_ASSIGNMENTS_PERMISSION)
        context["can_add_project_note"] = self.request.user.has_perm(ADD_PROJECT_NOTE_PERMISSION)

        if context["can_manage_assignments"]:
            context["assignment_form"] = ProjectAssignmentForm(project=project)

        if context["can_add_project_note"]:
            context["note_form"] = ProjectNoteForm()

        return context


class ProjectUpdateView(ProjectPermissionRequiredMixin, UpdateView):
    template_name = "projects/form.html"
    form_class = ProjectForm
    permission_required = CHANGE_PROJECT_PERMISSION
    queryset = Project.objects.select_related("client", "opportunity", "responsible")

    def form_valid(self, form):
        self.object = update_project(
            self.get_object(),
            data=form.cleaned_data,
            updated_by=self.request.user,
        )
        messages.success(self.request, "Project updated successfully.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("projects:detail", kwargs={"pk": self.object.pk})


class ProjectAssignmentCreateView(ProjectPermissionRequiredMixin, View):
    permission_required = MANAGE_ASSIGNMENTS_PERMISSION

    def post(self, request, pk, *args, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectAssignmentForm(request.POST, project=project)

        if form.is_valid():
            assign_user_to_project(
                project=project,
                user=form.cleaned_data["user"],
                role=form.cleaned_data["role"],
                assigned_by=request.user,
                notes=form.cleaned_data["notes"],
            )
            messages.success(request, "Assignment created successfully.")
        else:
            messages.error(request, "Could not create assignment. Review the submitted data.")

        return redirect("projects:detail", pk=project.pk)


class ProjectAssignmentDeactivateView(ProjectPermissionRequiredMixin, View):
    permission_required = MANAGE_ASSIGNMENTS_PERMISSION

    def post(self, request, pk, assignment_id, *args, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        assignment = get_object_or_404(ProjectAssignment, pk=assignment_id, project=project)

        try:
            deactivate_project_assignment(assignment=assignment, updated_by=request.user)
            messages.success(request, "Assignment deactivated successfully.")
        except ValidationError as exc:
            messages.error(request, exc.message)

        return redirect("projects:detail", pk=project.pk)


class ProjectNoteCreateView(ProjectPermissionRequiredMixin, View):
    permission_required = ADD_PROJECT_NOTE_PERMISSION

    def post(self, request, pk, *args, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectNoteForm(request.POST)

        if form.is_valid():
            add_project_note(
                project=project,
                author=request.user,
                body=form.cleaned_data["body"],
                note_type=form.cleaned_data["note_type"],
            )
            messages.success(request, "Project note created successfully.")
        else:
            messages.error(request, "Could not save the note. Review the submitted data.")

        return redirect("projects:detail", pk=project.pk)