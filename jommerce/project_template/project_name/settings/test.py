from .base import *


# General
# ----------------------------------------------------------------------------------------------------------------------
SECRET_KEY = "Fake Key"


# Apps
# ----------------------------------------------------------------------------------------------------------------------
INSTALLED_APPS += [
    "tests",
]


try:
    from .local import *
except ImportError:
    pass
