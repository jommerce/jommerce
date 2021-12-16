from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    @classmethod
    def normalize_email(cls, email):
        return super().normalize_email(email) if email else None
