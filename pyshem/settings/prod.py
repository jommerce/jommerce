from .base import *

DEBUG = False
ALLOWED_HOSTS = ['pyshem.com', 'www.pyshem.com']


STATIC_ROOT = os.environ['STATIC_ROOT']
MEDIA_ROOT = os.environ['MEDIA_ROOT']


try:
    from .local import *
except ImportError:
    pass
