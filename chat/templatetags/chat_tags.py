from django import template
from django.core import exceptions

from chat import models


register = template.Library()


@register.inclusion_tag("chat.html", takes_context=True)
def chat(context, chat_id):

    chat, _ = models.Chat.objects.get_or_create(chat_id=chat_id)

    context.update(dict(chat_id=chat_id, initial_messages=chat.messages_json(),))
    return context
