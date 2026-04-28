from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

urlpatterns = [
    path("", lambda request: redirect("dashboard/")),
    path("admin/", admin.site.urls),

    # Dashboard
    path(
        "dashboard/",
        TemplateView.as_view(template_name="dashboard/home.html"),
        name="dashboard_home",
    ),

    # Authentication
    path("accounts/", include("django.contrib.auth.urls")),
    path("i18n/", include("django.conf.urls.i18n")),

    # Apps
    path("users/", include("apps.users.urls")),
    path("clients/", include("apps.clients.urls")),
    path("sales/", include("apps.sales.urls")),
    path("projects/", include("apps.projects.urls")),
    path("workforce/", include("apps.workforce.urls")),
    path("media-assets/", include("apps.media_assets.urls")),
    path("visits/", include("apps.visits.urls")),
    path("billing/", include("apps.billing.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)