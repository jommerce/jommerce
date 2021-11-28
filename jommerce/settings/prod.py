from .base import *

DEBUG = False
ALLOWED_HOSTS = SECRETS.get('ALLOWED_HOSTS', [])


STATIC_ROOT = SECRETS['STATIC_ROOT']
MEDIA_ROOT = SECRETS['MEDIA_ROOT']


try:
    from .local import *
except ImportError:
    pass
