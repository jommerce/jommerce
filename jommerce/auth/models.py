from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from .fields import NullEmailField


class CustomUser(AbstractUser):
    email = NullEmailField(
        _("email address"), unique=True, null=True, blank=True, default=None
    )

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        app_label = "auth"
        db_table = "auth_user"

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        return super(CustomUser, self).save(*args, **kwargs)
