from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class User(models.Model):
    id = models.BigAutoField(_("ID"), primary_key=True)
    email = models.EmailField(_("email"), max_length=64, unique=True)
    password = models.CharField(_("password"), max_length=128)

    @property
    def is_superuser(self):
        return settings.AUTH_SUPERUSER_ID == self.id
