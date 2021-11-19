from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0']


# django-debug-toolbar
assert 'django.contrib.staticfiles' in INSTALLED_APPS
assert TEMPLATES[0]['BACKEND'] == 'django.template.backends.django.DjangoTemplates'
assert TEMPLATES[0]['APP_DIRS']
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1']


try:
    from .local import *
except ImportError:
    pass
