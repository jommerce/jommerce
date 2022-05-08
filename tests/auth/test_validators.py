from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from djplus.auth.validators import get_password_validators
from djplus.auth.validators import password as password_validators


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

    def test_validate_at_least_1_digit(self):
        validate = password_validators.number
        with self.assertRaisesMessage(ValidationError, "your password must contain at least 1 digit."):
            validate(
                'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
            )
        self.assertIsNone(validate("0123456789"))
        self.assertIsNone(validate("s%dfg$2lsf0@"))
        self.assertIsNone(validate("sS%tEe5&st_"))

    def test_validate_at_least_1_lowercase_letter(self):
        validate = password_validators.lowercase
        with self.assertRaisesMessage(ValidationError, "your password must contain at least 1 lowercase letter."):
            validate('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c')
        self.assertIsNone(validate("abcdefghijklmnopqrstuvwxyz"))
        self.assertIsNone(validate("S%32^Dd@31#$"))
        self.assertIsNone(validate("1~#GVzS%s5+f"))

    def test_validate_at_least_1_uppercase_letter(self):
        validate = password_validators.uppercase
        with self.assertRaisesMessage(ValidationError, "your password must contain at least 1 uppercase letter."):
            validate('0123456789abcdefghijklmnopqrstuvwxyz!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c')
        self.assertIsNone(validate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.assertIsNone(validate("s_32&Dd~31#*"))
        self.assertIsNone(validate("9~#HVzM%s0+f"))

    def test_validate_at_least_1_special_character(self):
        validate = password_validators.symbol
        with self.assertRaisesMessage(ValidationError, "your password must contain at least 1 special character."):
            validate('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ \t\n\r\x0b\x0c')
        self.assertIsNone(validate('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'))
        self.assertIsNone(validate("s6cm2%S30y"))
        self.assertIsNone(validate("s5FD#fs!4$3"))

    def test_password_must_be_at_least_8_characters_long(self):
        validate = password_validators.length
        with self.assertRaisesMessage(ValidationError, "your password must be at least 8 characters long."):
            validate('T$0@aYs')
        with self.assertRaisesMessage(ValidationError, "your password must be at least 8 characters long."):
            validate('Nm6$')
        self.assertIsNone(validate("m$dSC0#8"))
        self.assertIsNone(validate("m$@dFG(*3_0!No^"))
