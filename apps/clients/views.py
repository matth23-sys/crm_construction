from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ClientFilterForm, ClientForm, ClientInteractionForm
from .models import Client
from .permissions import ClientPermissionRequiredMixin
from .selectors import get_client_detail_queryset, get_clients_queryset
from .services import (
    create_client,
    deactivate_client,
    reactivate_client,
    register_client_interaction,
    update_client,
)


class ClientListView(LoginRequiredMixin, ClientPermissionRequiredMixin, ListView):
    model = Client
    template_name = "clients/list.html"
    context_object_name = "clients"
    paginate_by = 20
    permission_required = "clients.view_client"

    def get_filter_data(self):
        return {
            "search": self.request.GET.get("search", "").strip(),
            "status": self.request.GET.get("status", "").strip(),
            "client_type": self.request.GET.get("client_type", "").strip(),
        }

    def get_queryset(self):
        return get_clients_queryset(**self.get_filter_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = ClientFilterForm(self.request.GET or None)
        return context


class ClientCreateView(LoginRequiredMixin, ClientPermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/form.html"
    permission_required = "clients.add_client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Crear cliente"
        context["submit_label"] = "Guardar cliente"
        return context

    def form_valid(self, form):
        self.object = create_client(data=form.cleaned_data, user=self.request.user)
        messages.success(self.request, "Cliente creado correctamente.")
        return redirect(self.object.get_absolute_url())


class ClientUpdateView(LoginRequiredMixin, ClientPermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clients/form.html"
    permission_required = "clients.change_client"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Editar cliente"
        context["submit_label"] = "Guardar cambios"
        return context

    def form_valid(self, form):
        self.object = update_client(
            client=self.get_object(),
            data=form.cleaned_data,
            user=self.request.user,
        )
        messages.success(self.request, "Cliente actualizado correctamente.")
        return redirect(self.object.get_absolute_url())


class ClientDetailView(LoginRequiredMixin, ClientPermissionRequiredMixin, DetailView):
    model = Client
    template_name = "clients/detail.html"
    context_object_name = "client"
    permission_required = ("clients.view_client", "clients.view_clientinteraction")

    def get_queryset(self):
        return get_client_detail_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["interaction_form"] = ClientInteractionForm()
        return context


class ClientDeactivateView(LoginRequiredMixin, ClientPermissionRequiredMixin, View):
    permission_required = "clients.deactivate_client"

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        deactivate_client(client=client, user=request.user)
        messages.success(request, "Cliente desactivado correctamente.")
        return redirect(client.get_absolute_url())


class ClientReactivateView(LoginRequiredMixin, ClientPermissionRequiredMixin, View):
    permission_required = "clients.reactivate_client"

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        reactivate_client(client=client, user=request.user)
        messages.success(request, "Cliente reactivado correctamente.")
        return redirect(client.get_absolute_url())


class ClientInteractionCreateView(LoginRequiredMixin, ClientPermissionRequiredMixin, View):
    permission_required = "clients.add_clientinteraction"

    def post(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        form = ClientInteractionForm(request.POST)

        if form.is_valid():
            register_client_interaction(
                client=client,
                data=form.cleaned_data,
                user=request.user,
            )
            messages.success(request, "Interacción registrada correctamente.")
        else:
            messages.error(
                request,
                "No se pudo registrar la interacción. Revisa los datos enviados.",
            )

        return redirect(client.get_absolute_url())