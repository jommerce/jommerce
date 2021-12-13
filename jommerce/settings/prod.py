from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
    }
}

STATIC_ROOT = os.environ["STATIC_ROOT"]
MEDIA_ROOT = os.environ["MEDIA_ROOT"]


try:
    from .local import *
except ImportError:
    pass
