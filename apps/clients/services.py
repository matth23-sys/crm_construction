from django.db import transaction

from .models import Client, ClientInteraction


def _set_user_stamps(instance, user, *, creation=False):
    if not user or not getattr(user, "is_authenticated", False):
        return

    if creation and hasattr(instance, "created_by_id") and getattr(instance, "created_by_id", None) is None:
        instance.created_by = user

    if hasattr(instance, "updated_by_id"):
        instance.updated_by = user


def _apply_data(instance, data):
    for field_name, value in data.items():
        setattr(instance, field_name, value)


@transaction.atomic
def create_client(*, data, user=None) -> Client:
    client = Client()
    _apply_data(client, data)
    _set_user_stamps(client, user, creation=True)
    client.full_clean()
    client.save()
    return client


@transaction.atomic
def update_client(*, client: Client, data, user=None) -> Client:
    _apply_data(client, data)
    _set_user_stamps(client, user)
    client.full_clean()
    client.save()
    return client


@transaction.atomic
def deactivate_client(*, client: Client, user=None) -> Client:
    client.deactivate(user=user)
    _set_user_stamps(client, user)
    client.full_clean()
    client.save()
    return client


@transaction.atomic
def reactivate_client(*, client: Client, user=None) -> Client:
    client.reactivate()
    _set_user_stamps(client, user)
    client.full_clean()
    client.save()
    return client


@transaction.atomic
def register_client_interaction(*, client: Client, data, user=None) -> ClientInteraction:
    interaction = ClientInteraction(client=client)
    _apply_data(interaction, data)

    if user and getattr(user, "is_authenticated", False):
        interaction.registered_by = user

    _set_user_stamps(interaction, user, creation=True)
    interaction.full_clean()
    interaction.save()
    return interaction