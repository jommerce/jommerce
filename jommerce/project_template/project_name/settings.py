try:
    from .local_settings import *
except ImportError:
    from jommerce.settings.prod import *

ROOT_URLCONF = "{{ project_name }}.urls"
WSGI_APPLICATION = "{{ project_name }}.wsgi.application"
