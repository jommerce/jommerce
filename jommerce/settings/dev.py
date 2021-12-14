from .base import *

SECRET_KEY = "fake-key"

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]


try:
    import debug_toolbar
except ImportError:
    pass
else:
    INSTALLED_APPS.append("debug_toolbar")
    INTERNAL_IPS = ["127.0.0.1"]
    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )


try:
    from .local import *
except ImportError:
    pass
