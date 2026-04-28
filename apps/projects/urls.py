from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="list"),
    path("create/", views.ProjectCreateView.as_view(), name="create"),
    path(
        "create/from-opportunity/",
        views.ProjectCreateFromOpportunityView.as_view(),
        name="create_from_opportunity",
    ),
    path("<uuid:pk>/", views.ProjectDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", views.ProjectUpdateView.as_view(), name="edit"),
    path(
        "<uuid:pk>/assignments/add/",
        views.ProjectAssignmentCreateView.as_view(),
        name="assignment_create",
    ),
    path(
        "<uuid:pk>/assignments/<uuid:assignment_id>/deactivate/",
        views.ProjectAssignmentDeactivateView.as_view(),
        name="assignment_deactivate",
    ),
    path(
        "<uuid:pk>/notes/add/",
        views.ProjectNoteCreateView.as_view(),
        name="note_create",
    ),
]