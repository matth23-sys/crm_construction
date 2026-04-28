from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, FormView, TemplateView, View

from .forms import (
    ProjectPhotoFilterForm,
    ProjectPhotoReplaceForm,
    ProjectPhotoUploadForm,
)
from .permissions import (
    MediaAssetsPermissionRequiredMixin,
    ProjectLookupMixin,
    ProjectPhotoLookupMixin,
)
from .selectors import (
    get_project_gallery,
    get_project_gallery_counts,
)
from .services import create_project_photo, delete_project_photo, replace_project_photo


class ProjectGalleryView(
    LoginRequiredMixin,
    MediaAssetsPermissionRequiredMixin,
    ProjectLookupMixin,
    TemplateView,
):
    template_name = "media_assets/list.html"
    permission_required = "media_assets.view_project_gallery"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_project()
        filter_form = ProjectPhotoFilterForm(self.request.GET or None)

        filters = filter_form.cleaned_data if filter_form.is_valid() else {}
        photos = get_project_gallery(project=project, filters=filters)
        counts = get_project_gallery_counts(project)

        context.update(
            {
                "project": project,
                "filter_form": filter_form,
                "photos": photos,
                "classification_counts": counts,
                "can_upload": self.request.user.has_perm(
                    "media_assets.upload_projectphoto"
                ),
            }
        )
        return context


class ProjectPhotoUploadView(
    LoginRequiredMixin,
    MediaAssetsPermissionRequiredMixin,
    ProjectLookupMixin,
    FormView,
):
    template_name = "media_assets/form.html"
    form_class = ProjectPhotoUploadForm
    permission_required = "media_assets.upload_projectphoto"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["project"] = self.get_project()
        return kwargs

    def form_valid(self, form):
        project = self.get_project()
        photo = create_project_photo(
            project=project,
            image=form.cleaned_data["image"],
            classification=form.cleaned_data["classification"],
            actor=self.request.user,
            title=form.cleaned_data.get("title", ""),
            description=form.cleaned_data.get("description", ""),
            taken_at=form.cleaned_data.get("taken_at"),
        )
        messages.success(self.request, "Project photo uploaded successfully.")
        return redirect("media_assets:photo_detail", pk=photo.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "project": self.get_project(),
                "page_title": "Upload project photo",
                "submit_label": "Upload photo",
                "cancel_url": reverse(
                    "media_assets:project_gallery",
                    kwargs={"project_id": self.get_project().pk},
                ),
            }
        )
        return context


class ProjectPhotoDetailView(
    LoginRequiredMixin,
    MediaAssetsPermissionRequiredMixin,
    ProjectPhotoLookupMixin,
    DetailView,
):
    template_name = "media_assets/detail.html"
    context_object_name = "photo"
    permission_required = "media_assets.view_projectphoto"

    def get_object(self, queryset=None):
        return self.get_photo()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = self.get_photo()
        context.update(
            {
                "project": photo.project,
                "can_replace": self.request.user.has_perm(
                    "media_assets.replace_projectphoto"
                ),
                "can_delete": self.request.user.has_perm(
                    "media_assets.delete_projectphoto"
                ),
            }
        )
        return context


class ProjectPhotoReplaceView(
    LoginRequiredMixin,
    MediaAssetsPermissionRequiredMixin,
    ProjectPhotoLookupMixin,
    FormView,
):
    template_name = "media_assets/form.html"
    form_class = ProjectPhotoReplaceForm
    permission_required = "media_assets.replace_projectphoto"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        photo = self.get_photo()
        kwargs["instance"] = photo
        kwargs["project"] = photo.project
        return kwargs

    def form_valid(self, form):
        photo = self.get_photo()
        replace_project_photo(
            photo=photo,
            image=form.cleaned_data["image"],
            actor=self.request.user,
            classification=form.cleaned_data["classification"],
            title=form.cleaned_data.get("title", ""),
            description=form.cleaned_data.get("description", ""),
            taken_at=form.cleaned_data.get("taken_at"),
        )
        messages.success(self.request, "Project photo replaced successfully.")
        return redirect("media_assets:photo_detail", pk=photo.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = self.get_photo()
        context.update(
            {
                "project": photo.project,
                "photo": photo,
                "page_title": "Replace project photo",
                "submit_label": "Replace photo",
                "cancel_url": reverse(
                    "media_assets:photo_detail",
                    kwargs={"pk": photo.pk},
                ),
            }
        )
        return context


class ProjectPhotoDeleteView(
    LoginRequiredMixin,
    MediaAssetsPermissionRequiredMixin,
    ProjectPhotoLookupMixin,
    View,
):
    permission_required = "media_assets.delete_projectphoto"

    def post(self, request, *args, **kwargs):
        photo = self.get_photo()
        project_id = photo.project_id
        delete_project_photo(photo=photo)
        messages.success(request, "Project photo deleted successfully.")
        return redirect(
            "media_assets:project_gallery",
            project_id=project_id,
        )