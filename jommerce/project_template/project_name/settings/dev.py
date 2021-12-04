from jommerce.settings.dev import *
from .base import *


try:
    from .local import *
except ImportError:
    pass
