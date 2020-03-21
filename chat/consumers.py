import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat import models


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        self.chat, _ = models.Chat.objects.get_or_create(
            chat_id=self.chat_id,
            )

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name,
            self.channel_name
        )

        self.accept()

        # Send initial chat data
        self.send(text_data=json.dumps({
            'type': 'chat_init',
            'msgs': self.chat.messages_json(),
        }))



    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        author = text_data_json.get('author')

        if not author or not body:
            return

        # Save the message
        self.chat.add_message(body=body, author=author)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'body': body,
                'author': author,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': event['type'],
            'body': event['body'],
            'author': event['author'],
        }))
