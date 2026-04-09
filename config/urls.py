from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

handler403 = "apps.users.views.permission_denied_view"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="dashboard", permanent=False)),
    path("admin/", admin.site.urls),
    
    # Dashboard
    path("dashboard/", TemplateView.as_view(template_name="dashboard/home.html"), name="dashboard"),
    
    # Authentication
    path("accounts/", include("django.contrib.auth.urls")),
    
    # Apps
    path("users/", include("apps.users.urls")),
    path("clients/", include("apps.clients.urls")),
]