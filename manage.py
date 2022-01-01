#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import functools


def coverage(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cov = Coverage()
        cov.erase()
        cov.start()
        func(*args, **kwargs)
        cov.stop()
        cov.save()
        cov.report()
        cov.html_report(directory="htmlcov")

    try:
        from coverage import Coverage
    except ImportError:
        return func
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        return wrapper
    return func


@coverage
def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jommerce.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
