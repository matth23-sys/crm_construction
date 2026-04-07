from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_groups(sender, **kwargs):
    from .services import bootstrap_default_groups

    bootstrap_default_groups()


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    label = "users"
    verbose_name = "Users"

    def ready(self):
        post_migrate.connect(create_default_groups, sender=self)