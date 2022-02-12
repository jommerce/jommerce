import string
from django.test import TestCase
from django.core.exceptions import ValidationError
from jommerce.auth import validators


class PasswordValidators(TestCase):
    def test_at_least_one_number(self):
        with self.assertRaisesMessage(ValidationError, "Your password must contain at least 1 number."):
            validators.validate_password_number(string.ascii_letters + string.punctuation + string.whitespace)

        for number in string.digits:
            self.assertIsNone(validators.validate_password_number(number))

    def test_at_least_one_lowercase(self):
        with self.assertRaisesMessage(ValidationError, "Your password must contain at least 1 lowercase letter."):
            validators.validate_password_lowercase(string.ascii_uppercase + string.digits + string.punctuation + string.whitespace)

        for lowercase in string.ascii_lowercase:
            self.assertIsNone(validators.validate_password_lowercase(lowercase))

    def test_at_least_one_uppercase(self):
        with self.assertRaisesMessage(ValidationError, "Your password must contain at least 1 uppercase letter."):
            validators.validate_password_uppercase(string.ascii_lowercase + string.digits + string.punctuation + string.whitespace)

        for uppercase in string.ascii_uppercase:
            self.assertIsNone(validators.validate_password_uppercase(uppercase))

    def test_at_least_eight_characters(self):
        for i in range(8):
            with self.assertRaisesMessage(ValidationError, "Your password must contain at least 8 characters."):
                validators.validate_password_length("a" * i)

            self.assertIsNone(validators.validate_password_length("a" * (8 + i)))
