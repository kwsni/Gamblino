from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from .defaults import *

load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = getenv('DJANGO_SECRET_KEY')
DEBUG = getenv('DJANGO_DEBUG', 'True')
WSGI_APPLICATION = 'gamblino.wsgi.application'
LANGUAGE_CODE = getenv('DJANGO_LANGUAGE_CODE', 'en-us')
TIME_ZONE = getenv('DJANGO_TIME_ZONE', 'UTC')
USE_I18N = getenv('DJANGO_USE_I18N', 'True')
USE_TZ = getenv('DJANGO_USE_TZ', 'True')

ROOT_URLCONF = 'gamblino.urls'
STATIC_URL = '/static/'
STATIC_ROOT = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'

# Admin and email settings
#ADMINS = getenv('ADMINS')
EMAIL_HOST = getenv('DJANGO_EMAIL_HOST', '')
EMAIL_HOST_USER = getenv('DJANGO_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = getenv('DJANGO_EMAIL_HOST_PASSWORD', '')

INSTALLED_APPS = [
    'inventory.apps.InventoryConfig',
    'api.apps.ApiConfig',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.discord',

    'ninja',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',

    'allauth.account.middleware.AccountMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': getenv('DJANGO_DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': getenv('DJANGO_DB_NAME', BASE_DIR / "db.sqlite3"),
        'USER': getenv('DJANGO_DB_USER', 'gamblino'),
        'PASSWORD': getenv('DJANGO_DB_PASSWORD', 'nopassword'),
        'HOST': getenv('DJANGO_DB_HOST', '127.0.0.1'),
        'PORT': getenv('DJANGO_DB_PORT', '5432'),
    },
}

# Allauth settings

ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_VERIFICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
LOGIN_REDIRECT_URL = '/user/profile'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'discord': {
        'APPS': [
            {
                'client_id': getenv('DISCORD_APP_ID'),
                'secret': getenv('DISCORD_CLIENT_SECRET'),
                'key': getenv('DISCORD_PUBLIC_KEY'),
            },
        ],
        'SCOPE': [
            'email',
            'identify',
        ],
    }
}