import json
import logging

from asgiref.sync import async_to_sync
import channels
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat import models


log = logging.getLogger(__name__)

count = 0


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = await channels.auth.get_user(self.scope)
        if not user.is_authenticated:
            return

        global count
        count = count + 1

        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_group_name = f"chat_{self.chat_id}"

        self.chat, _ = await database_sync_to_async(models.Chat.objects.get_or_create)(
            chat_id=self.chat_id
        )

        log.info("user %r connected to chat %r", user, self.chat_id)

        # Join room group
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

        await self.accept()

        json_msgs = await database_sync_to_async(self.chat.messages_json)()

        # Send initial chat data
        await self.send(text_data=json.dumps({"type": "chat_init", "msgs": json_msgs,}))

        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name, {"type": "count_update", "count": count,}
        )

    async def disconnect(self, close_code):
        user = await channels.auth.get_user(self.scope)
        if not user.is_authenticated:
            return

        global count
        count = count - 1

        # Leave room group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

        await self.channel_layer.group_send(
            self.chat_group_name, {"type": "count_update", "count": count,}
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json["type"] == "chat":
            body = text_data_json["body"]
            kind = text_data_json["kind"]

            # Save the message
            user = await channels.auth.get_user(self.scope)
            msg = await database_sync_to_async(self.chat.add_message)(
                body=body, author=user, kind=kind
            )

            # Send message to room group
            await self.channel_layer.group_send(
                self.chat_group_name, {"type": "chat_message", **msg.__json__()}
            )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "type": event["type"],
                    "kind": event["kind"],
                    "body": event["body"],
                    "author": event["author"],
                    "created_at": event["created_at"],
                }
            )
        )

    async def count_update(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_connect(self, event):
        await self.send(text_data=json.dumps(event))
