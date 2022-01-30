from django.utils.translation import gettext_lazy as _
from django.db import models


class User(models.Model):
    email = models.EmailField(_("email"), max_length=64, unique=True)
    password = models.CharField(_("password"), max_length=128)
