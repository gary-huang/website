import os
from .base import *

DEBUG = False

SECRET_KEY = os.getenv("DJ_SECRET")

ALLOWED_HOSTS = [
    "crossroadschurch.ajax",
    "crossroadsinajax.xyz",
]

try:
    from .local import *
except ImportError:
    pass
