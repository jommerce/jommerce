from django.core.management.templates import TemplateCommand
from django.core.management.utils import get_random_secret_key
from pathlib import Path

PROJECT_TEMPLATE_DIR = Path(__file__).parent / "project_template"


def main():
    TemplateCommand().handle(
        "project",
        name=input("project_name[config]: ").strip() or "config",
        target=str(Path.cwd()),
        template=str(PROJECT_TEMPLATE_DIR),
        files=[".gitignore"],
        extensions=[".py", ".py-tpl"],
        exclude=[],
        verbosity=0,
    )
    print(f'SECRET_KEY = "{get_random_secret_key()}"')


if __name__ == "__main__":
    main()
