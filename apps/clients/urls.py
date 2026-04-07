from django.urls import path

from .views import (
    ClientCreateView,
    ClientDeactivateView,
    ClientDetailView,
    ClientInteractionCreateView,
    ClientListView,
    ClientReactivateView,
    ClientUpdateView,
)

app_name = "clients"

urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("create/", ClientCreateView.as_view(), name="create"),
    path("<uuid:pk>/", ClientDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", ClientUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/deactivate/", ClientDeactivateView.as_view(), name="deactivate"),
    path("<uuid:pk>/reactivate/", ClientReactivateView.as_view(), name="reactivate"),
    path(
        "<uuid:pk>/interactions/create/",
        ClientInteractionCreateView.as_view(),
        name="interaction_create",
    ),
]