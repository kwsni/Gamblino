from dotenv import load_dotenv

from .base import *

load_dotenv(override=True)

DEBUG = True
ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1', '192.168.0.0/24']