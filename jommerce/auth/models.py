from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from .fields import NullEmailField
from django.conf import settings
from django.db import models


class CustomUser(AbstractUser):
    email = NullEmailField(
        _("email address"),
        max_length=settings.AUTH_EMAIL_MAX_LENGTH,
        unique=True,
        null=True,
        blank=True,
        default=None,
    )
    first_name = models.CharField(
        _("first name"), max_length=settings.AUTH_FIRST_NAME_MAX_LENGTH, blank=True
    )
    last_name = models.CharField(
        _("last name"), max_length=settings.AUTH_LAST_NAME_MAX_LENGTH, blank=True
    )

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        abstract = "jommerce.auth" not in settings.INSTALLED_APPS
        app_label = "auth"
        db_table = "auth_user"

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        return super(CustomUser, self).save(*args, **kwargs)
