from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from djplus.auth.validators import validate_at_least_one_number, get_password_validators


def validate_return_none(value):
    pass


def validate_raise_error(value):
    raise ValidationError("fake message")


class PasswordValidatorsTest(TestCase):
    @override_settings()
    def test_get_password_validators(self):
        with self.settings(AUTH_PASSWORD_VALIDATORS=["tests.auth.test_validators.validate_return_none"]):
            self.assertListEqual(get_password_validators(), [validate_return_none])
        with self.settings(AUTH_PASSWORD_VALIDATORS=["tests.auth.test_validators.validate_raise_error"]):
            self.assertListEqual(get_password_validators(), [validate_raise_error])
        with self.settings(AUTH_PASSWORD_VALIDATORS=[
            "tests.auth.test_validators.validate_return_none",
            "tests.auth.test_validators.validate_raise_error",
        ]):
            self.assertListEqual(get_password_validators(), [validate_return_none, validate_raise_error])

    def test_validate_at_least_one_number(self):
        with self.assertRaisesMessage(ValidationError, "your password must contain at least one number."):
            validate_at_least_one_number(
                'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
            )
        self.assertIsNone(validate_at_least_one_number("0123456789"))
        self.assertIsNone(validate_at_least_one_number("s%dfg$2lsf0@"))
        self.assertIsNone(validate_at_least_one_number("sS%tEe5&st_"))
