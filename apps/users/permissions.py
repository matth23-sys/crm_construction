def can_manage_users(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)