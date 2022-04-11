from django.core.management import execute_from_command_line
from pathlib import Path

DIR_PROJECT_TEMPLATE = Path(__file__).parent / "project_template"


def main():
    execute_from_command_line([
        "django-admin",
        "startproject",
        "--template",
        str(DIR_PROJECT_TEMPLATE),
        "config",
        ".",
    ])


if __name__ == "__main__":
    main()
