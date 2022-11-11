from .base import *
from importlib.util import find_spec

# General
# ----------------------------------------------------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = "Fake Key"


# django-debug-toolbar
# ----------------------------------------------------------------------------------------------------------------------
if find_spec("debug_toolbar"):
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TEMPLATE_CONTEXT": True,
    }
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
