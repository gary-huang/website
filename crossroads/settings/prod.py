import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "crossroadsajax.church",
    "crossroadsinajax.xyz",
]

try:
    from .local import *
except ImportError:
    pass


# These are mounted by docker secrets.
# They are defined in prodstack.yml
def read_secret(secret):
    with open(f"/run/secrets/{secret}") as f:
        return f.read()

SECRET_KEY = read_secret("django_secret")

POSTMARK_API_KEY = read_secret("postmark_api_key")
