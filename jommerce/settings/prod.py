from .base import *

DEBUG = False
ALLOWED_HOSTS = ['jommerce.org', 'www.jommerce.org']


STATIC_ROOT = SECRETS['STATIC_ROOT']
MEDIA_ROOT = SECRETS['MEDIA_ROOT']


try:
    from .local import *
except ImportError:
    pass
