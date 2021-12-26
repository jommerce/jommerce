from jommerce.utils import inject_app_default_settings

inject_app_default_settings(f"{__name__}.settings", prefix="AUTH_")
