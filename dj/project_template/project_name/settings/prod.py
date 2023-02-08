from .base import *


# General
# ----------------------------------------------------------------------------------------------------------------------
DEBUG = False
ALLOWED_HOSTS += [
    "{{ domain_name }}",
]


try:
    from .local import *
except ImportError:
    pass
