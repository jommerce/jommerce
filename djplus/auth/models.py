from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .validators import get_password_validators, get_username_validators
from .utils import generate_random_string
from .hashers import get_hashers


class User(models.Model):
    email = models.EmailField(_("email"), max_length=64, unique=True)
    password = models.CharField(_("password"), max_length=128, validators=get_password_validators())

    __original_password = None

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_password = self.password

    def save(self, *args, **kwargs):
        if self.pk is None or self.__original_password != self.password:
            hasher = get_hashers()[0]
            self.password = hasher.hash(self.password)
        super().save(*args, **kwargs)
        self.__original_password = self.password

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def verify_password(self, raw_password):
        need_rehash = False
        for hasher in get_hashers():
            if hasher.verify(raw_password, self.password):
                if need_rehash:
                    self.password = raw_password
                    self.save()
                return True
            need_rehash = True
        return False


def generate_session_id():
    while True:
        session_id = generate_random_string(32)
        try:
            Session.objects.get(pk=session_id)
        except Session.DoesNotExist:
            return session_id


class Session(models.Model):
    id = models.CharField(_("id"), max_length=32, primary_key=True, default=generate_session_id)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions",
        verbose_name=_("user"),
        null=True,
        default=None,
    )
    data = models.JSONField(_("data"), default=dict, blank=True)

    modified = False
    accessed = False

    class Meta:
        verbose_name = _("session")
        verbose_name_plural = _("sessions")

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    @property
    def is_empty(self):
        return False if self.user or self.data else True

    def get(self, key, default=None, /):
        """ Return the value for key if key is in the dictionary, else default. """
        return self.data.get(key, default)

    def values(self):
        self.accessed = True
        return self.data.values()


class AnonymousUser:
    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return False
