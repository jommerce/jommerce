from django.test import TestCase
from django.core.exceptions import ValidationError
from djplus.auth.validators import validate_at_least_one_number


class PasswordValidatorsTest(TestCase):
    def test_validate_at_least_one_number(self):
        with self.assertRaisesMessage(ValidationError, "your password must contain at least one number."):
            validate_at_least_one_number(
                'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
            )
        self.assertIsNone(validate_at_least_one_number("0123456789"))
        self.assertIsNone(validate_at_least_one_number("s%dfg$2lsf0@"))
        self.assertIsNone(validate_at_least_one_number("sS%tEe5&st_"))
