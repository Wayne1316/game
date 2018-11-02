import os

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'charset': 'utf8mb4'},
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'NAME': os.environ.get('DB_NAME', ''),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWD', ''),
    }
}

DEBUG = True

ALLOWED_HOSTS += ['127.0.0.1']

# INSTALLED_APPS += ['debug_toolbar']

# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', 'core.middleware.XForwardedForMiddleware']

INTERNAL_IPS = ('127.0.0.1',)

LOGGING['handlers']['dev'] = {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'filename': os.path.join(LOG_DIR, 'dev.log'),
    'formatter': 'detail'
}

LOGGING['handlers']['header'] = {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'filename': os.path.join(LOG_DIR, 'header.log'),
    'formatter': 'detail'
}

LOGGING['loggers']['dev'] = {
    'handlers': ['dev'],
    'level': 'DEBUG',
    'propagate': True,
}

LOGGING['loggers']['header'] = {
    'handlers': ['header'],
    'level': 'DEBUG',
    'propagate': True,
}

SKIP_CAPTCHA = True
