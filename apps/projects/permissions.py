try:
    from apps.users.permissions import AppPermissionRequiredMixin as BaseAppPermissionRequiredMixin
except ImportError:  # pragma: no cover
    from django.contrib.auth.mixins import PermissionRequiredMixin as BaseAppPermissionRequiredMixin


VIEW_PROJECT_PERMISSION = "projects.view_project"
ADD_PROJECT_PERMISSION = "projects.add_project"
CHANGE_PROJECT_PERMISSION = "projects.change_project"
MANAGE_ASSIGNMENTS_PERMISSION = "projects.manage_assignments"
ADD_PROJECT_NOTE_PERMISSION = "projects.add_project_note"
CREATE_FROM_OPPORTUNITY_PERMISSION = "projects.create_project_from_opportunity"


class ProjectPermissionRequiredMixin(BaseAppPermissionRequiredMixin):
    """
    Reuses the permission strategy already defined in users.
    """
    pass