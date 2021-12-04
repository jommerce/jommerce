#!/usr/bin/env python
from django.core.management import execute_from_command_line
from pathlib import Path
import sys


JOMMERCE_DIR = Path(__file__).parent


def main():
    try:
        project_name = sys.argv[1]
    except IndexError:
        project_name = "config"

    execute_from_command_line(
        [
            "django-admin",
            "startproject",
            f"--template={str(JOMMERCE_DIR / 'project_template')}",
            "--name=secrets.toml",
            project_name,
            ".",
        ]
    )


if __name__ == "__main__":
    main()
