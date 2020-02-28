from django import template
from comments import models

register = template.Library()


@register.simple_tag
def comments_for(id):
    comments = models.Comment.objects.filter(thread_id="id").order_by("-created_at")


@register.inclusion_tag("comments_list.html", takes_context=True)
def render_comments_list(context, id):
    comments = models.Comment.objects.filter(thread_id="id").order_by("-created_at")
    return {
        "comments": comments,
    }


@register.inclusion_tag("comment_form.html", takes_context=True)
def render_comments_form(context, id):
    return {
        "form": None
    }
