from django.urls import path

from . import views

app_name = "workforce"

urlpatterns = [
    path("", views.MyProjectsListView.as_view(), name="list"),
    path("<uuid:pk>/", views.WorkforceProjectDetailView.as_view(), name="detail"),
    path("<uuid:pk>/notes/add/", views.WorkforceFieldNoteCreateView.as_view(), name="note_create"),
    path("<uuid:pk>/milestone/update/", views.WorkforceMilestoneUpdateView.as_view(), name="milestone_update"),
]