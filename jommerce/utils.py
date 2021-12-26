from django.utils.module_loading import import_module
from django.conf import settings


def inject_app_default_settings(settings_module, prefix: str = ""):
    try:
        conf = import_module(settings_module)
    except ImportError:
        raise ModuleNotFoundError(f"No module named '{settings_module}'")
    else:
        for key in filter(lambda x: x.isupper(), dir(conf)):
            key = prefix.upper() + key
            if not hasattr(settings, key):
                setattr(
                    settings,
                    key,
                    getattr(conf, key[len(prefix) :]),
                )
