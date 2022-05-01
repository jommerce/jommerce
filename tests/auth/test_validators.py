from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from djplus.auth.validators import (
    get_password_validators,
    validate_at_least_one_number,
    validate_at_least_one_lowercase,
    validate_at_least_one_uppercase,
)


def validate_return_none(value):
    pass


def validate_raise_error(value):
    raise ValidationError("fake message")


class PasswordValidatorsTest(TestCase):
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

    def test_validate_at_least_one_lowercase(self):
        with self.assertRaisesMessage(ValidationError, "your password must contain at least one lowercase letter."):
            validate_at_least_one_lowercase(
                '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
            )
        self.assertIsNone(validate_at_least_one_lowercase("abcdefghijklmnopqrstuvwxyz"))
        self.assertIsNone(validate_at_least_one_lowercase("S%32^Dd@31#$"))
        self.assertIsNone(validate_at_least_one_lowercase("1~#GVzS%s5+f"))

    def test_validate_at_least_one_uppercase(self):
        with self.assertRaisesMessage(ValidationError, "your password must contain at least one uppercase letter."):
            validate_at_least_one_uppercase(
                '0123456789abcdefghijklmnopqrstuvwxyz!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
            )
        self.assertIsNone(validate_at_least_one_uppercase("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.assertIsNone(validate_at_least_one_uppercase("s_32&Dd~31#*"))
        self.assertIsNone(validate_at_least_one_uppercase("9~#HVzM%s0+f"))
