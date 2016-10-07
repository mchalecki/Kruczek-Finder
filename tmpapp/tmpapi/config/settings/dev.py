# development settings
from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.child('db.sqlite3'),
    }
}

# Media files
MEDIA_ROOT = BASE_DIR.child("tmp")
MEDIA_URL = '/tmp/'

# Mailing
EMAIL_USE_TLS = True
EMAIL_HOST = get_secret("EMAIL_HOST") 
EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
