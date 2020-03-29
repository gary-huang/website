from django.conf import settings
from django.db import models


class ChatMessageReact(models.Model):
    item = models.ForeignKey(
        "ChatMessage", related_name="reacts", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="chat_reacts", on_delete=models.CASCADE
    )
    type = models.CharField(max_length=32)


class ChatMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length=2048)
    chat = models.ForeignKey("Chat", related_name="messages", on_delete=models.CASCADE)

    def aggreacts(self):
        # Aggregate common reacts into a list of tuples [(emoji, count)]
        aggr = []
        reacts = self.reacts.all()
        for react in "🙏,🙌,👋,➕".split(","):
            aggr.append((react, len(reacts.filter(type=react))))
        return aggr

    @classmethod
    def react(cls, user, msg_id, type):
        # Toggle a reaction
        msg = cls.objects.get(pk=msg_id)
        prev_reacts = ChatMessageReact.objects.filter(user=user, item=msg, type=type)
        if len(prev_reacts):
            for react in prev_reacts:
                react.delete()
        else:
            ChatMessageReact.objects.create(item=msg, user=user, type=type)

        return msg

    def __json__(self):
        return dict(
            id=self.pk,
            author=self.author.username,
            body=self.body,
            created_at=self.created_at.strftime("%s"),
            reacts=self.aggreacts(),
        )


class Chat(models.Model):
    chat_id = models.CharField(max_length=1024)

    def add_message(self, author, body=None):
        return ChatMessage.objects.create(
            author=author, body=body, chat=self,
        )

    def messages_json(self):
        return [msg.__json__() for msg in self.messages.all()]
