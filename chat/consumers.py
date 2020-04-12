from datetime import datetime
import json
import logging

from asgiref.sync import async_to_sync
import channels
from channels.db import database_sync_to_async as dbstoa
from channels.generic.websocket import AsyncWebsocketConsumer
from ddtrace import tracer, config as ddc

from chat import models
from church.models import User
from crossroads.consumers import SubConsumer, registry


log = logging.getLogger(__name__)


@registry.register
class ChatConsumer(SubConsumer):

    app_name = "chat"

    async def receive(self, user, data):
        print("RECEIVE %s %s" % (user, data))
        _type = data["type"]

        if _type == "chat.connect":
            self.chat_id = data["chat_id"]
            self.group_name = self.chat_id

            self.chat, _ = await dbstoa(
                models.Chat.objects.get_or_create
            )(chat_id=self.chat_id,)

            log.info("user %r connected to chat %r", user, self.chat_id)

            # Join room group
            await self.group_join(self.group_name)

            chat_json = await dbstoa(self.chat.__json__)()

            # Send initial chat data
            await self.send(text_data=json.dumps({"type": "chat.init", "chat": chat_json,}))

            # Send update message
            # await self.channel_layer.group_send(
            #     self.chat_group_name,
            #     {"type": "users_update", "users": ChatManager.user_list(self.chat_id)},
            # )
            # await self.group_send(self._group_name)

            await self.log("user_connect", user=user)
            pass

    async def log(self, type, user=None, body=""):
        log = await dbstoa(self.chat.add_log)(type=type, body=body, user=user,)

        # Send log to room group
        # log_json = await database_sync_to_async(log.__json__)()
        # await self.channel_layer.group_send(
        #     self.chat_group_name, {"type": "log", **log_json}
        # )

    async def handle(self, user, event):
        print("HANDLE %s %s" % (user, event))
        await self.send_json(event)


"""

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("CHAT CONNECT")

    async def chat_init(self, event):
        print("CHAT_INIT")
        return
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_group_name = f"chat_{self.chat_id}"

        with tracer.trace(
            "ws.chat_init", service=ddc.service, resource=f"WSS {self.chat_group_name}"
        ) as span:

            user = await channels.auth.get_user(self.scope)
            if not user.is_authenticated:
                return

            span.set_tag("user", user.username)

            self.chat, _ = await dbstoa(models.Chat.objects.get_or_create)(
                chat_id=self.chat_id,
            )

            log.info("user %r connected to chat %r", user, self.chat_id)

            # Join room group
            await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

            await self.accept()

            chat_json = await dbstoa(self.chat.__json__)()

            # Send initial chat data
            await self.send(text_data=json.dumps({"type": "init", "chat": chat_json,}))

            ChatManager.register(self.chat_id, user)
            # Send update message
            await self.channel_layer.group_send(
                self.chat_group_name,
                {"type": "users_update", "users": ChatManager.user_list(self.chat_id)},
            )

            await self.log("user_connect", user=user)


    async def disconnect(self, close_code):
        user = await channels.auth.get_user(self.scope)
        if not user.is_authenticated:
            return

        return

        ChatManager.deregister(self.chat_id, user)
        await self.log("user_disconnect", user=user)

        # Leave room group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

        # Update room with user count
        await self.channel_layer.group_send(
            self.chat_group_name,
            {"type": "users_update", "users": ChatManager.user_list(self.chat_id)},
        )

    async def receive(self, text_data):
        with tracer.trace("receive", resource=f"WSS {self.chat_group_name}") as span:
            text_data_json = json.loads(text_data)
            msgtype = text_data_json.get("type")
            span.set_tag("msg_type", msgtype)

            user = await channels.auth.get_user(self.scope)
            span.set_tag("user", user.username)

            if msgtype == "chat.message":
                body = text_data_json["body"]

                # Save the message
                msg = await dbstoa(self.chat.add_message)(body=body, author=user)

                # Send message to room group
                msg_json = await dbstoa(msg.__json__)()
                await self.channel_layer.group_send(
                    self.chat_group_name, {"type": "chat.message", **msg_json}
                )
            elif msgtype == "chat.react":
                msg_id = text_data_json["msg_id"]
                react = text_data_json["react"]
                span.set_tag("react", react)
                # Forward the react message to the rest of the clients
                msg = await dbstoa(models.ChatMessage.react)(user, msg_id, react)
                msg_json = await dbstoa(msg.__json__)()

                await self.channel_layer.group_send(
                    self.chat_group_name,
                    dict(type="chat_message_update", msg_id=msg_id, **msg_json,),
                )
            elif msgtype == "chat.toggle_pr":
                if not await dbstoa(user.has_perm)("chat.change_chatmessage"):
                    log.info("user %r tried to toggle pr without permissions", user)
                    return

                msg_id = text_data_json["msg_id"]
                msg = await dbstoa(models.ChatMessage.toggle_tag)("#pr", msg_id)
                msg_json = await dbstoa(msg.__json__)()
                await self.channel_layer.group_send(
                    self.chat_group_name,
                    dict(type="chat.message_update", msg_id=msg_id, **msg_json,),
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

"""
