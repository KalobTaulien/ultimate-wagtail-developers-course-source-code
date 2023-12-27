from .base import *  # noqa
import os
import sentry_sdk

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# -- Recommended CodeRed Cloud settings ---------------------------------------

ALLOWED_HOSTS = [os.environ["VIRTUAL_HOST"]]

SECRET_KEY = os.environ["RANDOM_SECRET_KEY"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Built-in email sending service provided by CodeRed Cloud.
# Change this to a different backend or SMTP server to use your own.
EMAIL_BACKEND = "django_sendmail_backend.backends.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ["DB_HOST"],
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "OPTIONS": {
            "client_encoding": "UTF8",
            "sslmode": "require",
        },
    }
}

WAGTAILADMIN_BASE_URL = f"http://{os.environ['VIRTUAL_HOST']}"


sentry_sdk.init(
    dsn="https://hehe-you-need-to-use-your-own-url.ingest.sentry.io/40404040404040",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
