from django.db import models
from .conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .validators import get_password_validators, get_username_validators
from .utils import generate_random_string
from .hashers import get_hashers


class User(models.Model):
    class Status(models.IntegerChoices):
        INACTIVE = 0
        ACTIVE = 1
    email = models.EmailField(_("email"), max_length=64, unique=True)
    password = models.CharField(_("password"), max_length=128, validators=get_password_validators())
    status = models.SmallIntegerField(_("status"), choices=Status.choices, default=Status.INACTIVE)

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


def get_default_expire_date():
    return timezone.now() + timezone.timedelta(seconds=settings.AUTH_SESSION_COOKIE_AGE)


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
    expire_date = models.DateTimeField(_("expire_date"), blank=True, default=get_default_expire_date)
    data = models.JSONField(_("data"), default=dict, blank=True)
    ip = models.GenericIPAddressField(_("IP"))

    modified = False
    accessed = False

    class Meta:
        verbose_name = _("session")
        verbose_name_plural = _("sessions")

    def __contains__(self, item):
        self.accessed = True
        return item in self.data

    def __getitem__(self, item):
        self.accessed = True
        return self.data[item]

    def __setitem__(self, key, value):
        self.modified = True
        self.data[key] = value

    def __delitem__(self, key):
        self.accessed = True
        self.modified = True
        del self.data[key]

    def save(self, *args, **kwargs):
        if self.user or self.data:
            return super().save(args, kwargs)

    def get(self, key, default=None):
        """ Return the value for key if key is in the dictionary, else default. """
        self.accessed = True
        return self.data.get(key, default)

    def values(self):
        self.accessed = True
        return self.data.values()

    def keys(self):
        self.accessed = True
        return self.data.keys()

    def items(self):
        self.accessed = True
        return self.data.items()

    def clear(self):
        self.accessed = True
        self.modified = True
        return self.data.clear()

    def setdefault(self, key, default=None):
        self.accessed = True
        if key not in self.data:
            self.modified = True
        return self.data.setdefault(key, default)

    def update(self, dictionary):
        self.accessed = True
        self.modified = True
        return self.data.update(dictionary)


class AnonymousUser:
    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return False
