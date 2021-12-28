from django.core.exceptions import ImproperlyConfigured
from jommerce.fields import NullEmailField
from .managers import CustomUserManager
from django.test import TestCase
from django.conf import settings
from .models import CustomUser


class DefaultSettingsTest(TestCase):
    def test_email_max_length(self):
        self.assertEqual(settings.AUTH_EMAIL_MAX_LENGTH, 40)


class CustomUserManagerTest(TestCase):
    def test_normalize_email(self):
        self.assertIsNone(CustomUserManager.normalize_email(None))
        self.assertIsNone(CustomUserManager.normalize_email(""))


class NullEmailFieldTest(TestCase):
    field = NullEmailField

    def test_null_true_blank_true(self):
        error_message = f"{self.field.__name__} implies null==blank==True"
        with self.assertRaisesMessage(ImproperlyConfigured, error_message):
            self.field(max_length=255, blank=True)
        with self.assertRaisesMessage(ImproperlyConfigured, error_message):
            self.field(max_length=255, null=True)
        with self.assertRaisesMessage(ImproperlyConfigured, error_message):
            self.field(max_length=255)
        try:
            self.field(max_length=255, null=True, blank=True)
        except ImproperlyConfigured:
            self.fail(f"{self.field.__name__} raised ImproperlyConfigured unexpectedly")

    def test_return_nona_as_empty_string(self):
        field = self.field(max_length=255, null=True, blank=True)
        self.assertEqual(field.to_python(None), "")
        self.assertIsNotNone(field.to_python(""))
        self.assertEqual(field.to_python(""), "")

    def test_store_empty_string_as_none(self):
        field = self.field(max_length=255, null=True, blank=True)
        self.assertIsNone(field.get_prep_value(""))


class CustomUserModelTest(TestCase):
    model = CustomUser

    def test_convert_empty_email_values_to_none(self):
        self.assertIsNone(self.model.objects.create(username="user1").email)
        self.assertIsNone(self.model.objects.create(username="user2", email="").email)
        self.assertIsNone(self.model.objects.create(username="user3", email=None).email)
        self.assertIsNone(self.model.objects.get(username="user1").email)
        self.assertIsNone(self.model.objects.get(username="user2").email)
        self.assertIsNone(self.model.objects.get(username="user3").email)
