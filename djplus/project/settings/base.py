from os import environ as SECRETS # noqa
from pathlib import Path

BASE_DIR = Path.cwd()
PROJECT_DIR = Path(__file__).resolve().parent.parent


# General
# ----------------------------------------------------------------------------------------------------------------------
SECRET_KEY = SECRETS.get("DJANGO_SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = SECRETS.get("DJANGO_ALLOWED_HOSTS", "").split()
ROOT_URLCONF = 'djplus.project.urls'
WSGI_APPLICATION = 'djplus.wsgi.application'


# Apps
# ----------------------------------------------------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.staticfiles",
]


# Middleware
# ----------------------------------------------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Templates
# ----------------------------------------------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]


# Databases
# ----------------------------------------------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Internationalization
# ----------------------------------------------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static and Media files
# ----------------------------------------------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    PROJECT_DIR / "static",
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
