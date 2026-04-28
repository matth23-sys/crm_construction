from django.urls import path

from . import views

app_name = "media_assets"

urlpatterns = [
    path(
        "projects/<uuid:project_id>/gallery/",
        views.ProjectGalleryView.as_view(),
        name="project_gallery",
    ),
    path(
        "projects/<uuid:project_id>/upload/",
        views.ProjectPhotoUploadView.as_view(),
        name="photo_upload",
    ),
    path(
        "photos/<uuid:pk>/",
        views.ProjectPhotoDetailView.as_view(),
        name="photo_detail",
    ),
    path(
        "photos/<uuid:pk>/replace/",
        views.ProjectPhotoReplaceView.as_view(),
        name="photo_replace",
    ),
    path(
        "photos/<uuid:pk>/delete/",
        views.ProjectPhotoDeleteView.as_view(),
        name="photo_delete",
    ),
]