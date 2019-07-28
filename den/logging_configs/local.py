import logging.config
import os

from django.utils.log import DEFAULT_LOGGING


def local_logging_config(**options):
    log_root = options.get('LOG_ROOT')
    log_level = options.get('LOG_LEVEL')
    file_log_level = options.get('FILE_LOG_LEVEL')
    sentry_log_level = options.get('SENTRY_LOG_LEVEL')

    return logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                # exact format is not important, this is the minimum information
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            },
            'django.server': DEFAULT_LOGGING['formatters']['django.server'],
        },
        'handlers': {
            # console logs to stderr
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },

            # # Add Handler for Sentry for `warning` and above
            'sentry': {
                'level': sentry_log_level,
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },

            # Adding file rotating log
            'file': {
                'level': file_log_level,
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': os.path.join(log_root, 'django.log'),
                'maxBytes': 50 * 1024 * 1024,  # 50 MB
                'backupCount': 20,
            },

            'django.server': DEFAULT_LOGGING['handlers']['django.server'],
        },
        'loggers': {
            # default for all undefined Python modules
            '': {
                'level': 'WARNING',
                'handlers': ['console', 'sentry', 'file'],
            },
            # Our application code
            'utils': {
                'level': log_level,
                'handlers': ['console', 'sentry', 'file'],
                # Avoid double logging because of root logger
                'propagate': False,
            },
            'knowledge': {
                'level': log_level,
                'handlers': ['console', 'sentry', 'file'],
                # Avoid double logging because of root logger
                'propagate': False,
            },
            'hustlers': {
                'level': log_level,
                'handlers': ['console', 'sentry', 'file'],
                # Avoid double logging because of root logger
                'propagate': False,
            },
            'integration': {
                'level': log_level,
                'handlers': ['console', 'sentry', 'file'],
                # Avoid double logging because of root logger
                'propagate': False,
            },
            # # Prevent noisy modules from logging to Sentry
            # 'noisy_module': {
            #     'level': 'ERROR',
            #     'handlers': ['console'],
            #     'propagate': False,
            # },
            # Default runserver request logging
            'django.server': DEFAULT_LOGGING['loggers']['django.server'],
        },
    })