from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from .validators import get_password_validators
from django.contrib.auth.hashers import make_password as hash_password, check_password


class User(models.Model):
    email = models.EmailField(_("email"), max_length=64, unique=True)
    password = models.CharField(_("password"), max_length=128, validators=get_password_validators())

    __original_password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_password = self.password

    def save(self, *args, **kwargs):
        if self.pk is None or self.__original_password != self.password:
            self.password = hash_password(self.password)
        super().save(*args, **kwargs)
        self.__original_password = self.password

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def is_superuser(self):
        return settings.AUTH_SUPERUSER_ID == self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
