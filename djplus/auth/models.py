from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
