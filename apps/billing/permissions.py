# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class BillingPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    raise_exception = True