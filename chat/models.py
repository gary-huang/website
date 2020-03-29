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


class ChatMessageTag(models.Model):
    value = models.CharField(max_length=32)
    item = models.ForeignKey(
        "ChatMessage", related_name="tags", on_delete=models.CASCADE
    )


class ChatMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length=2048)
    chat = models.ForeignKey("Chat", related_name="messages", on_delete=models.CASCADE)

    def aggreacts(self):
        # Aggregate common reacts into a list of tuples [(emoji, count)]
        aggr = []
        reacts = self.reacts.all()
        for react in "🙏,🙌,👋,➕,🤣".split(","):
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

    @staticmethod
    def _get_tags(s):
        return [w for w in s.split(" ") if w.startswith("#")]

    @staticmethod
    def _alias_tag(tag: str):
        tag = tag.lower()
        if tag.startswith("#"):
            tag = tag[1:]

        if tag in ["prayerrequest", "pr", "prayer", "pray", "pryr", "pry", "pyr"]:
            return "pr"
        if tag in ["q", "qna", "qa", "question", "q&a", "question"]:
            return "q"
        return tag

    def add_tag(self, raw_tag: str):
        tag = self._alias_tag(raw_tag)
        t, _ = ChatMessageTag.objects.get_or_create(item=self, value=tag)
        return t

    def add_tags(self, raw_tags=None):
        # Only meant to be called with #tags in place (not stripped yet)
        if isinstance(raw_tags, str):
            tags = self._get_tags(raw_tags)
        elif isinstance(raw_tags, []):
            tags = []
            for s in raw_tags:
                tags += self._get_tags(s)
        else:
            tags = self._get_tags(self.body)

        # create tags for the message
        for tag in tags:
            self.add_tag(tag)

    @classmethod
    def toggle_tag(cls, raw_tag, msg_id):
        cm = cls.objects.get(pk=msg_id)
        tag = cls._alias_tag(raw_tag)
        if tag in cm.raw_tags:
            tags = ChatMessageTag.objects.filter(item=cm, value=cls._alias_tag(tag))
            for t in tags:
                t.delete()
            return cm
        else:
            cm.add_tags(raw_tag)
        return cm

    @property
    def raw_tags(self):
        return [tag.value for tag in self.tags.all()]

    def __json__(self):
        return dict(
            id=self.pk,
            author=self.author.chat_name,
            body=self.body,
            created_at=self.created_at.strftime("%s"),
            reacts=self.aggreacts(),
            tags=self.raw_tags,
        )


class Chat(models.Model):
    chat_id = models.CharField(max_length=1024)

    def add_message(self, author, body=None):
        cm = ChatMessage.objects.create(author=author, body=body, chat=self,)
        cm.add_tags(body)
        return cm

    def messages_json(self):
        return [msg.__json__() for msg in self.messages.all()]
