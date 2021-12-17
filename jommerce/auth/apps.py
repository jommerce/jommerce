from jommerce.utils import set_default_settings
from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jommerce.auth"
    label = "jauth"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_default_settings(f"{self.name}.settings")
