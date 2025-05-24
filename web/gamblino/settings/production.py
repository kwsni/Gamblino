from os import getenv

from dotenv import load_dotenv

from .base import *

load_dotenv(override=True)

DEBUG = False
ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS').split(',')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
USE_X_FORWARDED_HOST = True

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.sftpstorage.SFTPStorage',
        'OPTIONS': {
            'host': getenv('DJANGO_STORAGE_HOST'),
            'root_path': getenv('DJANGO_STORAGE_MEDIA_ROOT'),
            'base_url': 'media/',
            'params': {
                'key_filename': getenv('DJANGO_STORAGE_SSH_KEY_PATH'),
            },
        },
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.sftpstorage.SFTPStorage',
        'OPTIONS': {
            'host': getenv('DJANGO_STORAGE_HOST'),
            'root_path': getenv('DJANGO_STORAGE_STATIC_ROOT'),
            'base_url': 'static/',
            'params': {
                'key_filename': getenv('DJANGO_STORAGE_SSH_KEY_PATH'),
            },
        },
    },
}
