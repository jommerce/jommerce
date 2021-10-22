from .base import *

DEBUG = False
ALLOWED_HOSTS = ['pyshem.com', 'www.pyshem.com']

try:
    from .local import *
except ImportError:
    pass
