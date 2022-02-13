from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def get_password_validators():
    return [import_string(validator) for validator in settings.AUTH_PASSWORD_VALIDATORS]


def validate_password_length(password):
    if len(password) < 8:
        raise ValidationError(
            _("Your password must contain at least 8 characters."),
            code="password_length",
        )


def validate_password_number(password):
    if not any(map(str.isdigit, password)):
        raise ValidationError(
            _("Your password must contain at least 1 number."),
            code="password_no_number",
        )


def validate_password_uppercase(password):
    if not any(map(str.isupper, password)):
        raise ValidationError(
            _("Your password must contain at least 1 uppercase letter."),
            code="password_no_uppercase",
        )


def validate_password_lowercase(password):
    if not any(map(str.islower, password)):
        raise ValidationError(
            _("Your password must contain at least 1 lowercase letter."),
            code="password_no_lowercase",
        )
