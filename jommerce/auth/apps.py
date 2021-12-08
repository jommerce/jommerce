from django.utils.module_loading import import_module
from django.apps import AppConfig
from django.conf import settings


class AuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jommerce.auth"
    label = "jauth"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)

        try:
            conf = import_module(self.name + ".settings")
        except ImportError:
            pass
        else:
            for name in filter(lambda x: x.isupper(), dir(conf)):
                if not hasattr(settings, name):
                    setattr(
                        settings,
                        name,
                        getattr(conf, name),
                    )
