from django.conf import settings as django_settings
from jommerce.auth import settings as app_settings


class Settings:
    def __getattribute__(self, item):
        try:
            return getattr(django_settings, item)
        except AttributeError:
            return getattr(app_settings, item)


settings = Settings()
