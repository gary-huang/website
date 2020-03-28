from django.conf import settings
from django.db import models


class ChatMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length=2048)
    chat = models.ForeignKey("Chat", related_name="messages", on_delete=models.CASCADE)
    kind = models.CharField(
        max_length=16, choices=[("PR", "pr"), ("CHAT", "chat")], default="CHAT"
    )

    def __json__(self):
        return dict(
            author=self.author.username,
            body=self.body,
            created_at=self.created_at.strftime("%s"),
            kind=self.kind,
        )


class Chat(models.Model):
    chat_id = models.CharField(max_length=1024)

    def add_message(self, author, body=None, kind=None):
        return ChatMessage.objects.create(
            author=author, body=body, chat=self, kind=kind
        )

    def messages_json(self):
        return [msg.__json__() for msg in self.messages.all()]
