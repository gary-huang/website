import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat import models

count = 0


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        global count
        count = count + 1
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_group_name = f"chat_{self.chat_id}"
        self.chat, _ = models.Chat.objects.get_or_create(chat_id=self.chat_id,)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name, self.channel_name
        )

        self.accept()

        # Send initial chat data
        self.send(
            text_data=json.dumps(
                {"type": "chat_init", "msgs": self.chat.messages_json(),}
            )
        )

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name, {"type": "count_update", "count": count,}
        )

    def disconnect(self, close_code):
        global count
        count = count - 1

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name, self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name, {"type": "count_update", "count": count,}
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json["type"] == "chat":
            body = text_data_json["body"]
            author = text_data_json.get("author")
            kind = text_data_json["kind"]

            if not author or not body:
                return

            # Save the message
            msg = self.chat.add_message(body=body, author=author, kind=kind)

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.chat_group_name, {"type": "chat_message", **msg.__json__()}
            )
        elif text_data_json["type"] == "username":
            author = text_data_json["author"]
            async_to_sync(self.channel_layer.group_send)(
                self.chat_group_name, {"type": "user_connect", "author": author,}
            )

    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(
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

    def count_update(self, event):
        self.send(text_data=json.dumps(event))

    def user_connect(self, event):
        self.send(text_data=json.dumps(event))
