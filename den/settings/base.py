"""
Django settings for den project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import raven
import datetime

from den.logging_configs.local import local_logging_config
from den.logging_configs.heroku import heroku_logging_config
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_bool(env_var):
    list_of_truth = [True, 'true', 'True', 1, '1']
    list_of_false = [False, 'false', 'False', 0, '0']

    if env_var in list_of_truth:
        return True
    elif env_var in list_of_false:
        return False
    else:
        return env_var


def get_env_variable(var_name):
    try:
        env_var = os.environ[var_name]
        return parse_bool(env_var)
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_env_variable('SECRET_KEY')

# TODO change this
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'rest_framework',
    'django_filters',
    'django_extensions',
    # installs a hook in Django that will automatically report uncaught exceptions.
    'raven.contrib.django.raven_compat',

    'django_celery_beat',

    #swagger app
    'rest_framework_swagger',
]

PROJECT_APPS = [
    'knowledge',
    'hustlers',
    'integrations',
    'utils',
]

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # project
    'utils.custom_error_handlers.HustlersDenExceptionMiddleware',
]

ROOT_URLCONF = 'den.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'den.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Authentication and REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
            'django_filters.rest_framework.DjangoFilterBackend',
        ),
}

JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'den.utils.auth_utils.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


JET_THEMES = [
    {
        'theme': 'default', # theme folder name
        'color': '#47bac1', # color of the theme's button in user menu
        'title': 'Default' # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

JET_SIDE_MENU_COMPACT = True
ADMIN_SITE_HEADER = "Hustlers Den"

# logging setup
# Disable Django's logging setup
LOGGING_CONFIG = None

# logs folder location where the file rotated logs are stored
LOG_ROOT = os.path.join(BASE_DIR, '..', 'logs')

# application log level
LOG_LEVEL = get_env_variable('ENV_LOG_LEVEL')

# separate log level for logging in Rotated file
FILE_LOG_LEVEL = get_env_variable('FILE_LOG_LEVEL')

# all logging including and above this level will be reported to Sentry
SENTRY_LOG_LEVEL = get_env_variable('SENTRY_LOG_LEVEL')


# Python logging on sentry, console and in file

logging_options = dict()
logging_options['LOG_ROOT'] = LOG_ROOT
logging_options['LOG_LEVEL'] = LOG_LEVEL
logging_options['FILE_LOG_LEVEL'] = FILE_LOG_LEVEL
logging_options['SENTRY_LOG_LEVEL'] = SENTRY_LOG_LEVEL

if get_env_variable('LOCAL_LOGGING'):
    local_logging_config(**logging_options)

else:
    heroku_logging_config(**logging_options)


# celery configuration
CELERY_BROKER_URL = get_env_variable('CELERY_RESULT_BACKEND')
CELERY_RESULT_BACKEND = get_env_variable('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
