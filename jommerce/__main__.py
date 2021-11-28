from django.core.management.utils import get_random_secret_key
from pathlib import Path
import json

ROOT_DIR = Path.cwd()

text = '''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
'''


def main():
    (ROOT_DIR / "settings.py").write_text("from jommerce.settings.prod import *\n")
    (ROOT_DIR / "local_settings.py").write_text("from jommerce.settings.dev import *\n")
    (ROOT_DIR / "manage.py").write_text(text)
    with open((ROOT_DIR / "secrets.json"), "w") as file:
        json.dump(
            {
                "SECRET_KEY": get_random_secret_key(),
                "ALLOWED_HOSTS": [
                    "example.com",
                    "www.example.com",
                ],
            },
            file,
            indent=4,
        )


if __name__ == "__main__":
    main()
