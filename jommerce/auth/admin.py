from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass
