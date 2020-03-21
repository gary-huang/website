from django.db import models


class ChatMessage(models.Model):
    author = models.CharField(max_length=256)
    body = models.CharField(max_length=2048)
    chat = models.ForeignKey("Chat", related_name="messages", on_delete=models.CASCADE)

    def __json__(self):
        return dict(
            author=self.author,
            body=self.body,
        )


class Chat(models.Model):
    chat_id = models.CharField(max_length=1024)

    def add_message(self, author=None, body=None):
        return ChatMessage.objects.create(author=author, body=body, chat=self)

    def messages_json(self):
        return [
            msg.__json__() for msg in self.messages.all()
        ]
