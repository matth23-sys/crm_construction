from django.http import HttpResponseRedirect


class RequestUserFormKwargsMixin:
    """Inyecta request.user al form como request_user."""

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request_user"] = self.request.user
        return kwargs


class AuditFieldsMixin:
    """
    Asigna created_by y updated_by cuando el modelo los tenga.
    Útil para CreateView y UpdateView.
    """

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if hasattr(self.object, "created_by") and not self.object.pk:
            self.object.created_by = self.request.user

        if hasattr(self.object, "updated_by"):
            self.object.updated_by = self.request.user

        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())