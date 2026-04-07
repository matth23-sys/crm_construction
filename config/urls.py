from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

from apps.users.views import (
    CRMLoginView,
    CRMLogoutView,
    CRMPasswordResetCompleteView,
    CRMPasswordResetConfirmView,
    CRMPasswordResetDoneView,
    CRMPasswordResetView,
)

handler403 = "apps.users.views.permission_denied_view"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="dashboard_home", permanent=False)),
    path("admin/", admin.site.urls),

    path("accounts/login/", CRMLoginView.as_view(), name="login"),
    path("accounts/logout/", CRMLogoutView.as_view(), name="logout"),
    path("accounts/password-reset/", CRMPasswordResetView.as_view(), name="password_reset"),
    path(
        "accounts/password-reset/done/",
        CRMPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        CRMPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        CRMPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

    path("users/", include(("apps.users.urls", "users"), namespace="users")),
    path(
        "dashboard/",
        TemplateView.as_view(template_name="dashboard/home.html"),
        name="dashboard_home",
    ),
]


