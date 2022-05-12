from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class PasswordLengthValidator:
    def __init__(self, min_length=8, max_length=100):
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, password):
        if len(password) < self.min_length:
            raise ValidationError(
                _("at least %(min_length)d characters"),
                code="password_too_short",
                params={"min_length": self.min_length},
            )
        elif self.max_length < len(password):
            raise ValidationError(
                _("at most %(max_length)d characters"),
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.min_length == other.min_length
            and self.max_length == other.max_length
        )


def number(password):
    if not any(map(str.isdigit, password)):
        raise ValidationError(
            _("at least one number"),
            code="password_no_number",
        )


def lowercase(password):
    if not any(map(str.islower, password)):
        raise ValidationError(
            _("at least one lowercase letter"),
            code="password_no_lowercase",
        )


def uppercase(password):
    if not any(map(str.isupper, password)):
        raise ValidationError(
            _("at least one uppercase letter"),
            code="password_no_uppercase",
        )


def symbol(password):
    special_characters = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    if not any(char in special_characters for char in password):
        raise ValidationError(
            _("at least one special character"),
            code="password_no_symbol",
        )


length = PasswordLengthValidator()
