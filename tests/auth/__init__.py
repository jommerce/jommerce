from django.core.signals import setting_changed
from django.dispatch import receiver
from djplus.auth.hashers import get_hashers


@receiver(setting_changed)
def reset_hashers(*, setting, **kwargs):
    if setting == "AUTH_PASSWORD_HASHERS":
        get_hashers.cache_clear()
