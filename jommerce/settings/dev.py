from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

try:
    from .local import *
except ImportError:
    pass
