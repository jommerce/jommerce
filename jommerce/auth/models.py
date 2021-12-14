from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True, null=True)

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        app_label = "auth"
        db_table = "auth_user"
