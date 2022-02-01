from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "jommerce.auth"
    verbose_name = _("Authentication and Authorization")

    def ready(self):
        from jommerce.auth import checks
