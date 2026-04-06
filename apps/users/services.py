def activate_user(user, *, commit=True):
    user.is_active = True
    if commit:
        user.save(update_fields=["is_active"])
    return user


def deactivate_user(user, *, commit=True):
    user.is_active = False
    if commit:
        user.save(update_fields=["is_active"])
    return user