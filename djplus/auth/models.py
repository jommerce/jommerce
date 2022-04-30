from django.db import models
from django.contrib.auth.hashers import make_password as hash_password


class User(models.Model):
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=128)

    __original_password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_password = self.password

    def save(self, *args, **kwargs):
        if self.pk is None or self.__original_password != self.password:
            self.password = hash_password(self.password)
        super().save(*args, **kwargs)
        self.__original_password = self.password
