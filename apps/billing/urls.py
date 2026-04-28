# -*- coding: utf-8 -*-

from django.urls import path

from apps.billing import views

app_name = "billing"

urlpatterns = [
    path("", views.AccountReceivableListView.as_view(), name="list"),
    path("pending/", views.PendingAccountReceivableListView.as_view(), name="pending"),
    path("create/", views.AccountReceivableCreateView.as_view(), name="create"),
    path("<uuid:pk>/", views.AccountReceivableDetailView.as_view(), name="detail"),
    path("<uuid:pk>/edit/", views.AccountReceivableUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/payments/register/", views.PaymentRegisterView.as_view(), name="payment_register"),
    path("<uuid:pk>/cancel/", views.AccountReceivableCancelView.as_view(), name="cancel"),
]