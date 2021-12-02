from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        app_label = "auth"
        db_table = "auth_user"
