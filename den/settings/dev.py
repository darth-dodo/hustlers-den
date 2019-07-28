from .base import *
import dj_database_url

DEBUG = get_env_variable('DEBUG_MODE')
HEROKU_MODE = get_env_variable('HEROKU_MODE')

if HEROKU_MODE:
    # https://stackoverflow.com/a/26080380/10400264
    DATABASE_URL = get_env_variable('DATABASE_URL')
    DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}


else:
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': get_env_variable('DATABASE_NAME'),
                'USER': get_env_variable('DATABASE_USER'),
                'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
                'HOST': get_env_variable('DATABASE_HOST'),
                'PORT': get_env_variable('DATABASE_PORT'),  # Set to empty string for default.
               }
    }


# enable/disable qcount
if True:

    MIDDLEWARE += [
                    'querycount.middleware.QueryCountMiddleware',
                ]

    QUERYCOUNT = {
        'THRESHOLDS': {
            'MEDIUM': 50,
            'HIGH': 200,
            'MIN_TIME_TO_LOG': 0,
            'MIN_QUERY_COUNT_TO_LOG': 0
        },
        'IGNORE_REQUEST_PATTERNS': [],
        'IGNORE_SQL_PATTERNS': [],
        'DISPLAY_DUPLICATES': 20,
    }


# enable/disable django debug toolbar
if True:
    INSTALLED_APPS += ['debug_toolbar', ]
    MIDDLEWARE += [
                   'debug_toolbar.middleware.DebugToolbarMiddleware',
                   ]

    # django debug toolbar allowed internal ips
    INTERNAL_IPS = ['127.0.0.1']

# sentry configuration only for env
SENTRY_SECRET_KEY = get_env_variable('SENTRY_SECRET_KEY')
SENTRY_PROJECT_ID = get_env_variable('SENTRY_PROJECT_ID')
SENTRY_DSN = 'https://{0}@sentry.io/{1}'.format(SENTRY_SECRET_KEY, SENTRY_PROJECT_ID)

RAVEN_CONFIG = {
    'dsn': SENTRY_DSN
}
