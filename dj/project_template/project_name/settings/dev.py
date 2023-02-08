from .base import *


# General
# ----------------------------------------------------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = "Fake Key"

{% if debug_toolbar %}
# django-debug-toolbar
# ----------------------------------------------------------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
{% endif %}


try:
    from .local import *
except ImportError:
    pass
