from django.core.exceptions import PermissionDenied

from .selectors import get_assigned_project_for_user


class AssignedProjectAccessMixin:
    project_url_kwarg = "pk"
    assigned_project = None

    def dispatch(self, request, *args, **kwargs):
        project_id = kwargs.get(self.project_url_kwarg)
        self.assigned_project = get_assigned_project_for_user(
            user=request.user,
            project_id=project_id,
        )

        if self.assigned_project is None:
            raise PermissionDenied("You do not have an active assignment for this project.")

        return super().dispatch(request, *args, **kwargs)