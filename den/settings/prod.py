from .base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env(
            "DATABASE_HOST"
        ),  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        "PORT": "",  # Set to empty string for default.
    }
}

# sentry configuration only for production env
SENTRY_SECRET_KEY = env("SENTRY_SECRET_KEY")
SENTRY_PROJECT_ID = env("SENTRY_PROJECT_ID")
SENTRY_DSN = "https://{0}@sentry.io/{1}".format(SENTRY_SECRET_KEY, SENTRY_PROJECT_ID)

RAVEN_CONFIG = {"dsn": SENTRY_DSN}
