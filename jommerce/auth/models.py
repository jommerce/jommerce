from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from .validators import get_password_validators


class User(models.Model):
    email = models.EmailField(_("email"), max_length=64, unique=True)
    password = models.CharField(_("password"), max_length=128, validators=get_password_validators())

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def is_superuser(self):
        return settings.AUTH_SUPERUSER_ID == self.id
