from .base import *


# General
# ----------------------------------------------------------------------------------------------------------------------
SECRET_KEY = "Fake Key"


# Apps
# ----------------------------------------------------------------------------------------------------------------------
INSTALLED_APPS += [
    "tests",
]


# Authentication
# ----------------------------------------------------------------------------------------------------------------------
AUTH_PASSWORD_HASHERS = ("tests.auth.test_hashers.pbkdf2_hasher",)
