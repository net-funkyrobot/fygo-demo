from os import path
from .base import *

DEBUG = False

with open(path.join(BASE_DIR, "secrets", "django_secret_key.txt")) as f:
    SECRET_KEY = f.read().strip()

# todo: Check AppEngine domain before first deployment
ALLOWED_HOSTS = ("funkyrobot-fygo-demo.appspot.com",)

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

# todo: Configure CloudSQL connection
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": "demodb",
#         "USER": "postgres",
#         "PASSWORD": "postgres",
#         "HOST": "db",
#         "PORT": "5432",
#     }
# }
