from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

import chat.consumers  # noqa this import is required to register the chat consumer
from . import consumers


application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter([re_path(r"ws/", consumers.Consumer),])
        ),
    }
)
