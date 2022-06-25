from django.core.management import execute_from_command_line
from django.core.management.utils import get_random_secret_key
from pathlib import Path

PROJECT_TEMPLATE_DIR = Path(__file__).parent / "project_template"


def main():
    project_name = input("project_name [config]: ").strip() or "config"
    execute_from_command_line([
        "django-admin",
        "startproject",
        "--template",
        str(PROJECT_TEMPLATE_DIR),
        "--name",
        ".gitignore",
        str(project_name),
        ".",
    ])
    print(f'SECRET_KEY = "{get_random_secret_key()}"')


if __name__ == "__main__":
    main()
