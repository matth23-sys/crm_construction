from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404

from apps.projects.models import Project

from .models import ProjectPhoto


class MediaAssetsPermissionRequiredMixin(PermissionRequiredMixin):
    raise_exception = True


class ProjectLookupMixin:
    project_url_kwarg = "project_id"
    _project = None

    def get_project(self):
        if self._project is None:
            self._project = get_object_or_404(
                Project.objects.select_related("client", "responsible"),
                pk=self.kwargs[self.project_url_kwarg],
            )
        return self._project


class ProjectPhotoLookupMixin:
    photo_url_kwarg = "pk"
    _photo = None

    def get_photo(self):
        if self._photo is None:
            self._photo = get_object_or_404(
                ProjectPhoto.objects.select_related(
                    "project",
                    "project__client",
                    "created_by",
                    "updated_by",
                ),
                pk=self.kwargs[self.photo_url_kwarg],
            )
        return self._photo