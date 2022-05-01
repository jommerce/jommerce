from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_at_least_one_number(password):
    if not any(map(str.isdigit, password)):
        raise ValidationError(
            _("your password must contain at least one number."),
            code="password_no_number",
        )
