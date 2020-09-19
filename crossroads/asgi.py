"""
"""

import os

import django
from channels.routing import get_default_application
from ddtrace.contrib.asgi import TraceMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crossroads.settings.prod")
django.setup()

application = TraceMiddleware(get_default_application())
