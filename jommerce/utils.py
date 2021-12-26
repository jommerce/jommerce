from django.utils.module_loading import import_module
from django.conf import settings, global_settings


def inject_app_default_settings(application: str, prefix=None):
    """Inject an application's default settings"""
    try:
        conf = import_module(f"{application}.settings")
    except ImportError:
        raise ModuleNotFoundError(f"No module named '{application}.settings'")
    else:
        if prefix is None:
            prefix = getattr(conf, "prefix", "").upper()
        for key in filter(lambda k: k.isupper(), dir(conf)):
            default = getattr(conf, key)
            key = prefix + key
            setattr(global_settings, key, default)
            if not hasattr(settings, key):
                setattr(settings, key, default)
