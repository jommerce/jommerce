from django.core.exceptions import ImproperlyConfigured
from jommerce.utils.models.fields import NullEmailField
from django.test import TestCase


class NullEmailFieldTests(TestCase):
    field = NullEmailField

    def test_null_true_blank_true(self):
        error_message = f"{self.field.__name__} implies null==blank==True"
        with self.assertRaisesMessage(ImproperlyConfigured, error_message):
            self.field(max_length=254, blank=True)
        with self.assertRaisesMessage(ImproperlyConfigured, error_message):
            self.field(max_length=254, null=True)
        with self.assertRaisesMessage(ImproperlyConfigured, error_message):
            self.field(max_length=254)
        try:
            self.field(max_length=254, null=True, blank=True)
        except ImproperlyConfigured:
            self.fail(f"{self.field.__name__} raised ImproperlyConfigured unexpectedly")

    def test_return_nona_as_empty_string(self):
        field = self.field(max_length=254, null=True, blank=True)
        self.assertEqual(field.to_python(None), "")
        self.assertIsNotNone(field.to_python(""))
        self.assertEqual(field.to_python(""), "")

    def test_store_empty_string_as_none(self):
        field = self.field(max_length=254, null=True, blank=True)
        self.assertIsNone(field.get_prep_value(""))
