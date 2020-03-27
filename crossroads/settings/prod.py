import os
from .base import *

DEBUG = False

SECRET_KEY = os.getenv("DJ_SECRET")

try:
    from .local import *
except ImportError:
    pass
