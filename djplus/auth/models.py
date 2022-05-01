from django.db import models
from django.contrib.auth.hashers import make_password as hash_password, check_password
from .validators import get_password_validators


class User(models.Model):
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=128, validators=get_password_validators())

    __original_password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_password = self.password

    def save(self, *args, **kwargs):
        if self.pk is None or self.__original_password != self.password:
            self.password = hash_password(self.password)
        super().save(*args, **kwargs)
        self.__original_password = self.password

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
