from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from jommerce.auth.validators import UsernameLengthValidator


def identifier(username: str):
    if not username.isidentifier():
        raise ValidationError(
            _(
                (
                    "Your username must be a combination of letters or digits or an underscore "
                    "and cannot start with a digit."
                )
            ),
            code="username_no_identifier",
        )


def ascii(username: str):
    if not username.isascii():
        raise ValidationError(
            _("Your username characters must be ASCII."),
            code="username_no_ascii",
        )


length = UsernameLengthValidator()
