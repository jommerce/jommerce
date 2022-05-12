from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from djplus.auth.validators import get_password_validators
from djplus.auth.validators import password as password_validators
from djplus.auth.validators.password import PasswordLengthValidator


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
        validate = password_validators.number
        with self.assertRaisesMessage(ValidationError, "at least one number"):
            validate(
                'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
            )
        self.assertIsNone(validate("0123456789"))
        self.assertIsNone(validate("s%dfg$2lsf0@"))
        self.assertIsNone(validate("sS%tEe5&st_"))

    def test_validate_at_least_one_lowercase_letter(self):
        validate = password_validators.lowercase
        with self.assertRaisesMessage(ValidationError, "at least one lowercase letter"):
            validate('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c')
        self.assertIsNone(validate("abcdefghijklmnopqrstuvwxyz"))
        self.assertIsNone(validate("S%32^Dd@31#$"))
        self.assertIsNone(validate("1~#GVzS%s5+f"))

    def test_validate_at_least_one_uppercase_letter(self):
        validate = password_validators.uppercase
        with self.assertRaisesMessage(ValidationError, "at least one uppercase letter"):
            validate('0123456789abcdefghijklmnopqrstuvwxyz!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c')
        self.assertIsNone(validate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.assertIsNone(validate("s_32&Dd~31#*"))
        self.assertIsNone(validate("9~#HVzM%s0+f"))

    def test_validate_at_least_one_special_character(self):
        validate = password_validators.symbol
        with self.assertRaisesMessage(ValidationError, "at least one special character"):
            validate('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ \t\n\r\x0b\x0c')
        self.assertIsNone(validate('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'))
        self.assertIsNone(validate("s6cm2%S30y"))
        self.assertIsNone(validate("s5FD#fs!4$3"))

    def test_validate_password_length(self):
        validate_between_8_and_16_characters = PasswordLengthValidator(min_length=8, max_length=16)
        validate_between_6_and_20_characters = PasswordLengthValidator(min_length=6, max_length=20)

        with self.assertRaisesMessage(ValidationError, "at least 8 characters") as err:
            validate_between_8_and_16_characters("T$0@aYs")
        self.assertEqual(err.exception.code, "password_too_short")

        with self.assertRaisesMessage(ValidationError, "at most 16 characters") as err:
            validate_between_8_and_16_characters('Bh:d]4G9i*5Y-dv?k>t%&c')
        self.assertEqual(err.exception.code, "password_too_long")

        with self.assertRaisesMessage(ValidationError, "at least 6 characters") as err:
            validate_between_6_and_20_characters("Nm6$")
        self.assertEqual(err.exception.code, "password_too_short")

        with self.assertRaisesMessage(ValidationError, "at most 20 characters") as err:
            validate_between_6_and_20_characters('mk%*G;-(&T_?^x=Z-hw0DD')
        self.assertEqual(err.exception.code, "password_too_long")

        self.assertIsNone(validate_between_8_and_16_characters("m$dSC0#8"))
        self.assertIsNone(validate_between_8_and_16_characters("ml|&6UErZk{&"))
        self.assertIsNone(validate_between_8_and_16_characters("N`{@T%!/z_~*22rm"))

        self.assertIsNone(validate_between_6_and_20_characters("<{2|N&"))
        self.assertIsNone(validate_between_6_and_20_characters("*q[*%'=k9kRo{a!_TI"))
        self.assertIsNone(validate_between_6_and_20_characters("m$@dFG(*3_0!No^$#i-b"))

        validate_between_8_and_20_characters = PasswordLengthValidator(min_length=8, max_length=20)
        self.assertNotEqual(validate_between_8_and_16_characters, validate_between_8_and_20_characters)
        self.assertNotEqual(validate_between_6_and_20_characters, validate_between_8_and_20_characters)
        self.assertNotEqual(validate_between_6_and_20_characters, validate_between_8_and_16_characters)
        self.assertEqual(validate_between_8_and_16_characters, PasswordLengthValidator(min_length=8, max_length=16))
