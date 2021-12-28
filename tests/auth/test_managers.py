from jommerce.auth.managers import CustomUserManager
from django.test import TestCase


class CustomUserManagerTests(TestCase):
    def test_normalize_email(self):
        self.assertIsNone(CustomUserManager.normalize_email(None))
        self.assertIsNone(CustomUserManager.normalize_email(""))
