from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from djplus.auth.validators import get_password_validators, get_username_validators
from djplus.auth.validators import password as password_validators
from djplus.auth.validators.password import PasswordLengthValidator
from djplus.auth.validators.username import UsernameLengthValidator


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


class UsernameValidatorsTest(TestCase):
    def test_get_username_validators(self):
        with self.settings(AUTH_USERNAME_VALIDATORS=["tests.auth.test_validators.validate_return_none"]):
            self.assertListEqual(get_username_validators(), [validate_return_none])
        with self.settings(AUTH_USERNAME_VALIDATORS=["tests.auth.test_validators.validate_raise_error"]):
            self.assertListEqual(get_username_validators(), [validate_raise_error])
        with self.settings(AUTH_USERNAME_VALIDATORS=[
            "tests.auth.test_validators.validate_return_none",
            "tests.auth.test_validators.validate_raise_error",
        ]):
            self.assertListEqual(get_username_validators(), [validate_return_none, validate_raise_error])


class UsernameLengthValidatorTests(TestCase):
    def test_raise_when_min_length_is_equal_to_or_less_than_zero(self):
        expected_message = "The 'min_length' argument must be greater than zero or None"
        for num in (0, -1, -2):
            with self.assertRaisesMessage(ValueError, expected_message):
                UsernameLengthValidator(min_length=num)

    def test_raise_when_max_length_is_equal_to_or_less_than_zero(self):
        expected_message = "The 'max_length' argument must be greater than zero or None"
        for num in (0, -1, -2):
            with self.assertRaisesMessage(ValueError, expected_message):
                UsernameLengthValidator(max_length=num)

    def test_raise_when_min_length_greater_than_max_length(self):
        expected_message = "The 'min_length' argument must be less than the 'max_length' argument"
        with self.assertRaisesMessage(ValueError, expected_message):
            UsernameLengthValidator(min_length=32, max_length=5)
        with self.assertRaisesMessage(ValueError, expected_message):
            UsernameLengthValidator(min_length=4, max_length=3)

    def test_raise_when_both_min_length_and_max_length_arguments_are_none(self):
        expected_message = "Both 'min_length' and 'max_length' arguments cannot be None"
        with self.assertRaisesMessage(ValueError, expected_message):
            UsernameLengthValidator(min_length=None, max_length=None)

    def test_validate_with_min_length_and_max_length(self):
        validate_between_6_and_32_characters = UsernameLengthValidator(min_length=6, max_length=32)

        expected_message = "Your username must be at least 6 characters long."
        with self.assertRaisesMessage(ValidationError, expected_message) as err:
            validate_between_6_and_32_characters("admin")
        self.assertEqual(err.exception.code, "username_too_short")

        expected_message = "Your username must be at most 32 characters long."
        with self.assertRaisesMessage(ValidationError, expected_message) as err:
            validate_between_6_and_32_characters("username_too_looooooooooooooooong")
        self.assertEqual(err.exception.code, "username_too_long")

        self.assertIsNone(validate_between_6_and_32_characters("python"))
        self.assertIsNone(validate_between_6_and_32_characters("developer"))
        self.assertIsNone(validate_between_6_and_32_characters("a" * 32))

    def test_validate_just_with_max_length(self):
        validate_at_most_30_characters = UsernameLengthValidator(min_length=None, max_length=30)

        expected_message = "Your username must be at most 30 characters long."
        with self.assertRaisesMessage(ValidationError, expected_message) as err:
            validate_at_most_30_characters("a" * 32)
        self.assertEqual(err.exception.code, "username_too_long")

        self.assertIsNone(validate_at_most_30_characters(""))
        self.assertIsNone(validate_at_most_30_characters("django"))
        self.assertIsNone(validate_at_most_30_characters("b" * 30))

    def test_validate_just_with_min_length(self):
        validate_at_least_5_characters = UsernameLengthValidator(min_length=5, max_length=None)

        expected_message = "Your username must be at least 5 characters long."
        with self.assertRaisesMessage(ValidationError, expected_message) as err:
            validate_at_least_5_characters("test")
        self.assertEqual(err.exception.code, "username_too_short")

        self.assertIsNone(validate_at_least_5_characters("admin"))
        self.assertIsNone(validate_at_least_5_characters("javascript"))
        self.assertIsNone(validate_at_least_5_characters("c" * 255))

    def test_equal_method(self):
        validate_between_5_and_32_characters = UsernameLengthValidator(min_length=5, max_length=32)
        validate_at_most_32_characters = UsernameLengthValidator(min_length=None, max_length=32)
        validate_at_least_5_characters = UsernameLengthValidator(min_length=5, max_length=None)

        self.assertNotEqual(validate_between_5_and_32_characters, validate_at_least_5_characters)
        self.assertNotEqual(validate_between_5_and_32_characters, validate_at_most_32_characters)
        self.assertNotEqual(validate_at_least_5_characters, validate_at_most_32_characters)

        validate_between_6_and_32_characters = UsernameLengthValidator(min_length=6, max_length=32)
        validate_between_5_and_30_characters = UsernameLengthValidator(min_length=5, max_length=30)
        validate_between_6_and_30_characters = UsernameLengthValidator(min_length=6, max_length=30)

        self.assertNotEqual(validate_between_5_and_32_characters, validate_between_6_and_32_characters)
        self.assertNotEqual(validate_between_5_and_32_characters, validate_between_5_and_30_characters)
        self.assertNotEqual(validate_between_5_and_32_characters, validate_between_6_and_30_characters)

        self.assertEqual(validate_between_5_and_32_characters, UsernameLengthValidator(min_length=5, max_length=32))
        self.assertEqual(validate_at_least_5_characters, UsernameLengthValidator(min_length=5, max_length=None))
        self.assertEqual(validate_at_most_32_characters, UsernameLengthValidator(min_length=None, max_length=32))
