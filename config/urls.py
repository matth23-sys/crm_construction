from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import include, path
from django.views.generic import TemplateView


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")
    return redirect("login")


dashboard_view = login_required(
    TemplateView.as_view(template_name="dashboard/home.html")
)

urlpatterns = [
    path("", root_redirect, name="root"),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/", include("apps.users.urls")),
    path("dashboard/", dashboard_view, name="dashboard_home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)