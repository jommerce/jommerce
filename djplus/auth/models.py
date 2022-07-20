from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .validators import get_password_validators, get_username_validators
from .hashers import get_hashers


class User(models.Model):
    ACTIVE = 0
    INACTIVE = 1

    username = models.CharField(_("username"), max_length=32, unique=True, validators=get_username_validators())
    email = models.EmailField(_("email"), max_length=64, unique=True)
    password = models.CharField(_("password"), max_length=128, validators=get_password_validators())
    status = models.SmallIntegerField(_("status"), default=ACTIVE, choices=(
        (ACTIVE, _("active")),
        (INACTIVE, _("inactive")),
    ))

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


class Session(models.Model):
    id = models.CharField(_("id"), max_length=32, primary_key=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions",
        verbose_name=_("user"),
        null=True,
        default=None,
    )
    expire_date = models.DateTimeField(_("expire_date"), db_index=True)
    ip = models.GenericIPAddressField(_("ip"))

    class Meta:
        verbose_name = _("session")
        verbose_name_plural = _("sessions")


class AnonymousUser:
    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return False
