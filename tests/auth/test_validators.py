from django.test import TestCase
from django.core.exceptions import ValidationError
from jommerce.auth.validators import (
    get_password_validators,
    get_username_validators,
    UsernameLengthValidator,
    PasswordLengthValidator,
)
from jommerce.auth.validators import password as password_validators
from jommerce.auth.validators import username as username_validators


def validate_return_none(value):
    pass


def validate_raise_error(value):
    raise ValidationError("fake message")


class PasswordValidatorsTest(TestCase):
    def test_get_password_validators(self):
        with self.settings(
            AUTH_PASSWORD_VALIDATORS=[
                "tests.auth.test_validators.validate_return_none",
                "tests.auth.test_validators.validate_raise_error",
            ]
        ):
            self.assertListEqual(
                get_password_validators(), [validate_return_none, validate_raise_error]
            )

        with self.settings(
            AUTH_PASSWORD_VALIDATORS=[
                "tests.auth.test_validators.validate_raise_error",
                "tests.auth.test_validators.validate_return_none",
            ]
        ):
            self.assertListEqual(
                get_password_validators(), [validate_raise_error, validate_return_none]
            )

    def test_validate_at_least_one_number(self):
        validate = password_validators.number
        with self.assertRaisesMessage(ValidationError, "at least one number"):
            validate(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
            )
        self.assertIsNone(validate("0123456789"))
        self.assertIsNone(validate("s%dfg$2lsf0@"))
        self.assertIsNone(validate("sS%tEe5&st_"))

    def test_validate_at_least_one_lowercase_letter(self):
        validate = password_validators.lowercase
        with self.assertRaisesMessage(ValidationError, "at least one lowercase letter"):
            validate(
                "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
            )
        self.assertIsNone(validate("abcdefghijklmnopqrstuvwxyz"))
        self.assertIsNone(validate("S%32^Dd@31#$"))
        self.assertIsNone(validate("1~#GVzS%s5+f"))

    def test_validate_at_least_one_uppercase_letter(self):
        validate = password_validators.uppercase
        with self.assertRaisesMessage(ValidationError, "at least one uppercase letter"):
            validate(
                "0123456789abcdefghijklmnopqrstuvwxyz!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
            )
        self.assertIsNone(validate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.assertIsNone(validate("s_32&Dd~31#*"))
        self.assertIsNone(validate("9~#HVzM%s0+f"))

    def test_validate_at_least_one_special_character(self):
        validate = password_validators.symbol
        with self.assertRaisesMessage(
            ValidationError, "at least one special character"
        ):
            validate("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.assertIsNone(validate("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"))
        self.assertIsNone(validate("s6cm2%S30y"))
        self.assertIsNone(validate("s5FD#fs!4$3"))


class UsernameValidatorsTest(TestCase):
    def test_get_username_validators(self):
        with self.settings(
            AUTH_USERNAME_VALIDATORS=[
                "tests.auth.test_validators.validate_raise_error",
                "tests.auth.test_validators.validate_return_none",
            ]
        ):
            self.assertListEqual(
                get_username_validators(), [validate_raise_error, validate_return_none]
            )

        with self.settings(
            AUTH_USERNAME_VALIDATORS=[
                "tests.auth.test_validators.validate_return_none",
                "tests.auth.test_validators.validate_raise_error",
            ]
        ):
            self.assertListEqual(
                get_username_validators(), [validate_return_none, validate_raise_error]
            )

    def test_validate_identifier(self):
        validate = username_validators.identifier
        expected_message = (
            "Your username must be a combination of letters or digits or an underscore "
            "and cannot start with a digit."
        )
        for string in ["9user", "test user", "invalid$"]:
            with self.assertRaisesMessage(ValidationError, expected_message) as err:
                validate(string)
            self.assertEqual(err.exception.code, "username_no_identifier")

        for string in ["staff", "test_username", "user1234", "user_01234"]:
            self.assertIsNone(validate(string))

    def test_validate_ascii(self):
        validate = username_validators.ascii
        expected_message = "Your username characters must be ASCII."
        for invalid in ["ᴮᴵᴳᴮᴵᴿᴰ", "Éric", "René", "أحمد", "ぁ"]:
            with self.subTest(invalid=invalid):
                with self.assertRaisesMessage(ValidationError, expected_message) as err:
                    validate(invalid)
                self.assertEqual(err.exception.code, "username_no_ascii")

        for valid in ["glenn", "GLEnN", "jean#marc", "user_2022"]:
            with self.subTest(valid=valid):
                self.assertIsNone(validate(valid))


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
        expected_message = (
            "The 'min_length' argument must be less than the 'max_length' argument"
        )
        with self.assertRaisesMessage(ValueError, expected_message):
            UsernameLengthValidator(min_length=32, max_length=5)
        with self.assertRaisesMessage(ValueError, expected_message):
            UsernameLengthValidator(min_length=4, max_length=3)

    def test_raise_when_both_min_length_and_max_length_arguments_are_none(self):
        expected_message = "Both 'min_length' and 'max_length' arguments cannot be None"
        with self.assertRaisesMessage(ValueError, expected_message):
            UsernameLengthValidator(min_length=None, max_length=None)

    def test_validate_with_min_length_and_max_length(self):
        validate_between_6_and_32_characters = UsernameLengthValidator(
            min_length=6, max_length=32
        )

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
        validate_at_most_30_characters = UsernameLengthValidator(
            min_length=None, max_length=30
        )

        expected_message = "Your username must be at most 30 characters long."
        with self.assertRaisesMessage(ValidationError, expected_message) as err:
            validate_at_most_30_characters("a" * 32)
        self.assertEqual(err.exception.code, "username_too_long")

        self.assertIsNone(validate_at_most_30_characters(""))
        self.assertIsNone(validate_at_most_30_characters("django"))
        self.assertIsNone(validate_at_most_30_characters("b" * 30))

    def test_validate_just_with_min_length(self):
        validate_at_least_5_characters = UsernameLengthValidator(
            min_length=5, max_length=None
        )

        expected_message = "Your username must be at least 5 characters long."
        with self.assertRaisesMessage(ValidationError, expected_message) as err:
            validate_at_least_5_characters("test")
        self.assertEqual(err.exception.code, "username_too_short")

        self.assertIsNone(validate_at_least_5_characters("admin"))
        self.assertIsNone(validate_at_least_5_characters("javascript"))
        self.assertIsNone(validate_at_least_5_characters("c" * 255))

    def test_equal_method(self):
        validate_between_5_and_32_characters = UsernameLengthValidator(
            min_length=5, max_length=32
        )
        validate_at_most_32_characters = UsernameLengthValidator(
            min_length=None, max_length=32
        )
        validate_at_least_5_characters = UsernameLengthValidator(
            min_length=5, max_length=None
        )

        self.assertNotEqual(
            validate_between_5_and_32_characters, validate_at_least_5_characters
        )
        self.assertNotEqual(
            validate_between_5_and_32_characters, validate_at_most_32_characters
        )
        self.assertNotEqual(
            validate_at_least_5_characters, validate_at_most_32_characters
        )

        validate_between_6_and_32_characters = UsernameLengthValidator(
            min_length=6, max_length=32
        )
        validate_between_5_and_30_characters = UsernameLengthValidator(
            min_length=5, max_length=30
        )
        validate_between_6_and_30_characters = UsernameLengthValidator(
            min_length=6, max_length=30
        )

        self.assertNotEqual(
            validate_between_5_and_32_characters, validate_between_6_and_32_characters
        )
        self.assertNotEqual(
            validate_between_5_and_32_characters, validate_between_5_and_30_characters
        )
        self.assertNotEqual(
            validate_between_5_and_32_characters, validate_between_6_and_30_characters
        )

        self.assertEqual(
            validate_between_5_and_32_characters,
            UsernameLengthValidator(min_length=5, max_length=32),
        )
        self.assertEqual(
            validate_at_least_5_characters,
            UsernameLengthValidator(min_length=5, max_length=None),
        )
        self.assertEqual(
            validate_at_most_32_characters,
            UsernameLengthValidator(min_length=None, max_length=32),
        )


class PasswordLengthValidatorTests(TestCase):
    def test_raise_when_min_length_is_equal_to_or_less_than_zero(self):
        expected_message = "The 'min_length' argument must be greater than zero or None"
        for num in (0, -1, -2):
            with self.assertRaisesMessage(ValueError, expected_message):
                PasswordLengthValidator(min_length=num)

    def test_raise_when_max_length_is_equal_to_or_less_than_zero(self):
        expected_message = "The 'max_length' argument must be greater than zero or None"
        for num in (0, -1, -2):
            with self.assertRaisesMessage(ValueError, expected_message):
                PasswordLengthValidator(max_length=num)

    def test_raise_when_min_length_greater_than_max_length(self):
        expected_message = (
            "The 'min_length' argument must be less than the 'max_length' argument"
        )
        with self.assertRaisesMessage(ValueError, expected_message):
            PasswordLengthValidator(min_length=100, max_length=8)
        with self.assertRaisesMessage(ValueError, expected_message):
            PasswordLengthValidator(min_length=6, max_length=5)

    def test_raise_when_both_min_length_and_max_length_arguments_are_none(self):
        expected_message = "Both 'min_length' and 'max_length' arguments cannot be None"
        with self.assertRaisesMessage(ValueError, expected_message):
            PasswordLengthValidator(min_length=None, max_length=None)

    def test_validate_with_min_length_and_max_length(self):
        validate_between_8_and_100_characters = PasswordLengthValidator(
            min_length=8, max_length=100
        )

        expected_message = "Your password must be at least 8 characters long."
        with self.assertRaisesMessage(ValidationError, expected_message) as err:
            validate_between_8_and_100_characters("T$0@aYs")
        self.assertEqual(err.exception.code, "password_too_short")

        expected_message = "Your password must be at most 100 characters long."
        with self.assertRaisesMessage(ValidationError, expected_message) as err:
            validate_between_8_and_100_characters("a" * 101)
        self.assertEqual(err.exception.code, "password_too_long")

        self.assertIsNone(validate_between_8_and_100_characters("password"))
        self.assertIsNone(
            validate_between_8_and_100_characters("l_dfj$34#lkjfs434_*sl3")
        )
        self.assertIsNone(validate_between_8_and_100_characters("a" * 100))

    def test_validate_just_with_max_length(self):
        validate_at_most_10_characters = PasswordLengthValidator(
            min_length=None, max_length=10
        )

        expected_message = "Your password must be at most 10 characters long."
        with self.assertRaisesMessage(ValidationError, expected_message) as err:
            validate_at_most_10_characters("a" * 11)
        self.assertEqual(err.exception.code, "password_too_long")

        self.assertIsNone(validate_at_most_10_characters(""))
        self.assertIsNone(validate_at_most_10_characters("django"))
        self.assertIsNone(validate_at_most_10_characters("b" * 10))

    def test_validate_just_with_min_length(self):
        validate_at_least_5_characters = PasswordLengthValidator(
            min_length=5, max_length=None
        )

        expected_message = "Your password must be at least 5 characters long."
        with self.assertRaisesMessage(ValidationError, expected_message) as err:
            validate_at_least_5_characters("test")
        self.assertEqual(err.exception.code, "password_too_short")

        self.assertIsNone(validate_at_least_5_characters("admin"))
        self.assertIsNone(validate_at_least_5_characters("javascript"))
        self.assertIsNone(validate_at_least_5_characters("c" * 255))

    def test_equal_method(self):
        validate_between_5_and_32_characters = PasswordLengthValidator(
            min_length=5, max_length=32
        )
        validate_at_most_32_characters = PasswordLengthValidator(
            min_length=None, max_length=32
        )
        validate_at_least_5_characters = PasswordLengthValidator(
            min_length=5, max_length=None
        )

        self.assertNotEqual(
            validate_between_5_and_32_characters, validate_at_least_5_characters
        )
        self.assertNotEqual(
            validate_between_5_and_32_characters, validate_at_most_32_characters
        )
        self.assertNotEqual(
            validate_at_least_5_characters, validate_at_most_32_characters
        )

        validate_between_6_and_32_characters = PasswordLengthValidator(
            min_length=6, max_length=32
        )
        validate_between_5_and_30_characters = PasswordLengthValidator(
            min_length=5, max_length=30
        )
        validate_between_6_and_30_characters = PasswordLengthValidator(
            min_length=6, max_length=30
        )

        self.assertNotEqual(
            validate_between_5_and_32_characters, validate_between_6_and_32_characters
        )
        self.assertNotEqual(
            validate_between_5_and_32_characters, validate_between_5_and_30_characters
        )
        self.assertNotEqual(
            validate_between_5_and_32_characters, validate_between_6_and_30_characters
        )

        self.assertEqual(
            validate_between_5_and_32_characters,
            PasswordLengthValidator(min_length=5, max_length=32),
        )
        self.assertEqual(
            validate_at_least_5_characters,
            PasswordLengthValidator(min_length=5, max_length=None),
        )
        self.assertEqual(
            validate_at_most_32_characters,
            PasswordLengthValidator(min_length=None, max_length=32),
        )
