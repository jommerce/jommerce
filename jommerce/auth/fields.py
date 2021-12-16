from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from django.db.models import EmailField


class NullEmailField(EmailField):
    """
    Subclass of the EmailField that allows empty strings to be stored as NULL in database.
    Useful when using unique=True and forms. Implies null==blank==True.
    Django's EmailField stores '' as None, but does not return None as ''.
    """

    description = _("EmailField that stores '' as None and returns None as ''")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.blank or not self.null:
            raise ImproperlyConfigured("NullEmailField implies null==blank==True")

    def to_python(self, value):
        val = super().to_python(value)
        return "" if val is None else val

    def get_prep_value(self, value):
        prep_value = super().get_prep_value(value)
        return None if prep_value == "" else prep_value
