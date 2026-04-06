from django.contrib.auth import get_user_model

User = get_user_model()


def get_active_users():
    return User.objects.filter(is_active=True).order_by("username")


def get_user_by_id(user_id):
    return User.objects.filter(pk=user_id).first()