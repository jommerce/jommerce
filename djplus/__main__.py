from django.core.management.templates import TemplateCommand
from django.core.management.utils import get_random_secret_key
from pathlib import Path
import json

PROJECT_TEMPLATE_DIR = Path(__file__).parent / "project_template"


def generate_config_file():
    with open(Path.home() / "djplus.json", "w") as file:
        json.dump({
            "debug_toolbar": True,
            "argon2": True,
        }, file, indent=4)


def main():
    try:
        with open(Path.home() / "djplus.json") as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {}

    TemplateCommand().handle(
        "project",
        name=input("project_name[config]: ").strip() or "config",
        target=str(Path.cwd()),
        template=str(PROJECT_TEMPLATE_DIR),
        files=[".gitignore"],
        extensions=[".py", ".py-tpl", ".txt"],
        exclude=[],
        verbosity=0,

        secret_key=get_random_secret_key(),
        domain_name=input("domain_name[example.local]: ").strip() or "example.local",
        **config,
    )


if __name__ == "__main__":
    main()
