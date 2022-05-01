from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string
from django.conf import settings


def get_password_validators():
    return [import_string(validator) for validator in settings.AUTH_PASSWORD_VALIDATORS]


def validate_at_least_one_number(password):
    if not any(map(str.isdigit, password)):
        raise ValidationError(
            _("your password must contain at least one number."),
            code="password_no_number",
        )


def validate_at_least_one_lowercase(password):
    if not any(map(str.islower, password)):
        raise ValidationError(
            _("your password must contain at least one lowercase letter."),
            code="password_no_lowercase",
        )


def validate_at_least_one_uppercase(password):
    if not any(map(str.isupper, password)):
        raise ValidationError(
            _("your password must contain at least one uppercase letter."),
            code="password_no_uppercase",
        )


def validate_at_least_1_special_character(password):
    pass
