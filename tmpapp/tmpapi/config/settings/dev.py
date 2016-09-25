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
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'by.mail.testing@gmail.com'
EMAIL_HOST_PASSWORD = 'QWE123asd'
EMAIL_PORT = 587
