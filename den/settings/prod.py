from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': get_env_variable('DATABASE_HOST'),  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
       }
}

# sentry configuration only for production env
SENTRY_SECRET_KEY = get_env_variable('SENTRY_SECRET_KEY')
SENTRY_PROJECT_ID = get_env_variable('SENTRY_PROJECT_ID')
SENTRY_DSN = 'https://{0}@sentry.io/{1}'.format(SENTRY_SECRET_KEY, SENTRY_PROJECT_ID)

RAVEN_CONFIG = {
    'dsn': SENTRY_DSN
}
