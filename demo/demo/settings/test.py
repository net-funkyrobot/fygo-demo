from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "t99sx&xi!y87udjx(uz0i64!snw=9p&yeu%h(5zj#du&=u(4w!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
