from django.core.checks import Error, register
from django.conf import settings
from jommerce.auth.models import User


@register()
def check_superuser_id(app_configs, **kwargs):
    errors = []
    if isinstance(settings.AUTH_SUPERUSER_ID, int):
        if User.objects.exists() or settings.AUTH_SUPERUSER_ID != 1:
            if not User.objects.filter(id=settings.AUTH_SUPERUSER_ID).exists():
                errors.append(
                    Error(
                        f"Couldn't find User with id={settings.AUTH_SUPERUSER_ID}",
                        hint="Change the 'AUTH_SUPERUSER_ID' value or create a user with that ID.",
                        obj=User,
                        id="auth.E002",
                    )
                )
    else:
        errors.append(
            Error(
                "'AUTH_SUPERUSER_ID' must be an integer",
                id="auth.E001",
            )
        )
    return errors
