from django.core.management import execute_from_command_line


def main():
    execute_from_command_line([
        "django-admin",
        "startproject",
        "config",
        ".",
    ])


if __name__ == "__main__":
    main()
