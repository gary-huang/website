from datetime import datetime
import json
import logging

from asgiref.sync import async_to_sync
import channels
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat import models
from church.models import User


log = logging.getLogger(__name__)


class Chatbot:

    # user.pk: timestamp (seconds)
    connect_time = {}

    # user.username: dict(user=user, count=int)
    users = {}

    @classmethod
    def register(cls, user):
        cls.users[user.username] = cls.users.get(
            user.username, dict(user=user, count=0)
        )
        cls.users[user.username]["count"] += 1

    @classmethod
    def deregister(cls, user):
        if user.username in cls.users:
            cls.users[user.username]["count"] -= 1

    @classmethod
    def user_list(cls):
        return [
            dict(username=username, count=meta["count"])
            for username, meta in cls.users.items()
            if meta["count"] > 0
        ]

    @classmethod
    def should_send_connect(cls, user):
        # If there exists a gap of 5 minutes from when the user
        # last connected, then show another message
        pk = user.pk
        this_time = int(datetime.now().strftime("%s"))
        try:
            if pk not in cls.connect_time:
                cls.connect_time[pk] = this_time
                return True
            else:
                last_time = cls.connect_time[pk]
                # After 5 minutes
                if this_time - last_time > 60 * 5:
                    return True
                return False
        finally:
            cls.connect_time[pk] = this_time


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = await channels.auth.get_user(self.scope)
        if not user.is_authenticated:
            return

        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_group_name = f"chat_{self.chat_id}"

        self.chatbot, _ = await database_sync_to_async(User.objects.get_or_create)(
            username="chatbot"
        )
        self.chat, _ = await database_sync_to_async(models.Chat.objects.get_or_create)(
            chat_id=self.chat_id,
        )

        log.info("user %r connected to chat %r", user, self.chat_id)

        # Join room group
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

        await self.accept()

        json_msgs = await database_sync_to_async(self.chat.messages_json)()

        # Send initial chat data
        await self.send(text_data=json.dumps({"type": "chat_init", "msgs": json_msgs,}))

        Chatbot.register(user)
        # Send update message
        await self.channel_layer.group_send(
            self.chat_group_name, {"type": "users_update", "users": Chatbot.user_list()}
        )

        # Create welcome message for user
        body = f"{user.username} has joined the service! 😊"
        if Chatbot.should_send_connect(user):
            await self.chatbotmsg(body)

    async def chatbotmsg(self, body, type=None):
        msg = await database_sync_to_async(self.chat.add_message)(
            body=body, author=self.chatbot
        )

        # Send message to room group
        msg_json = await database_sync_to_async(msg.__json__)()
        await self.channel_layer.group_send(
            self.chat_group_name, {"type": "chat_message", **msg_json}
        )

    async def disconnect(self, close_code):
        user = await channels.auth.get_user(self.scope)
        if not user.is_authenticated:
            return

        Chatbot.deregister(user)

        # Leave room group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

        await self.channel_layer.group_send(
            self.chat_group_name, {"type": "users_update", "users": Chatbot.user_list()}
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        user = await channels.auth.get_user(self.scope)

        if text_data_json["type"] == "chat_message":
            body = text_data_json["body"]

            # Save the message
            msg = await database_sync_to_async(self.chat.add_message)(
                body=body, author=user
            )

            # Send message to room group
            msg_json = await database_sync_to_async(msg.__json__)()
            await self.channel_layer.group_send(
                self.chat_group_name, {"type": "chat_message", **msg_json}
            )
        elif text_data_json["type"] == "chat_react":
            msg_id = text_data_json["msg_id"]
            react = text_data_json["react"]
            # Forward the react message to the rest of the clients
            msg = await database_sync_to_async(models.ChatMessage.react)(
                user, msg_id, react
            )
            msg_json = await database_sync_to_async(msg.__json__)()

            await self.channel_layer.group_send(
                self.chat_group_name,
                dict(type="chat_message_update", msg_id=msg_id, **msg_json,),
            )
        elif text_data_json["type"] == "chat_toggle_pr":
            if not await database_sync_to_async(user.has_perm)(
                "chat.change_chatmessage"
            ):
                log.info("user %r tried to toggle pr without permissions", user)
                return

            msg_id = text_data_json["msg_id"]
            msg = await database_sync_to_async(models.ChatMessage.toggle_tag)(
                "#pr", msg_id
            )
            msg_json = await database_sync_to_async(msg.__json__)()
            await self.channel_layer.group_send(
                self.chat_group_name,
                dict(type="chat_message_update", msg_id=msg_id, **msg_json,),
            )

    # Receive message from room group
    async def chat_message_update(self, event):
        # Forward message to WebSocket
        await self.send(text_data=json.dumps(event))

    # Receive message from room group
    async def chat_message(self, event):
        # Forward message to WebSocket
        await self.send(text_data=json.dumps(event))

    async def users_update(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_connect(self, event):
        await self.send(text_data=json.dumps(event))
