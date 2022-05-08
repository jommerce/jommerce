from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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


def length(password):
    if len(password) < 8:
        raise ValidationError(
            _("at least 8 characters"),
            code="password_length",
        )
