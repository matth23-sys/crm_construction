from django.urls import path

from .views import (
    AccessDeniedView,
    AccessLogListView,
    ProfileView,
    RoleCreateView,
    RoleListView,
    RoleUpdateView,
    UserActivateView,
    UserCreateView,
    UserDeactivateView,
    UserDetailView,
    UserListView,
    UserUpdateView,
)

app_name = "users"

urlpatterns = [
    path("", UserListView.as_view(), name="list"),
    path("create/", UserCreateView.as_view(), name="create"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("roles/", RoleListView.as_view(), name="role_list"),
    path("roles/create/", RoleCreateView.as_view(), name="role_create"),
    path("roles/<int:pk>/edit/", RoleUpdateView.as_view(), name="role_update"),
    path("access-logs/", AccessLogListView.as_view(), name="access_log_list"),
    path("access-denied/", AccessDeniedView.as_view(), name="access_denied"),
    path("<uuid:pk>/", UserDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", UserUpdateView.as_view(), name="update"),
    path("<uuid:pk>/activate/", UserActivateView.as_view(), name="activate"),
    path("<uuid:pk>/deactivate/", UserDeactivateView.as_view(), name="deactivate"),
]