from jommerce.auth import settings as app_settings
from django.test import TestCase
from django.conf import settings


class DefaultSettingsTests(TestCase):
    def test_prefix(self):
        self.assertEqual(app_settings.prefix, "AUTH_")

    def test_email_max_length(self):
        self.assertEqual(settings.AUTH_EMAIL_MAX_LENGTH, 40)
