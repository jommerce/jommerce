from jommerce.settings.prod import *
from .base import *


try:
    from .local import *
except ImportError:
    pass
