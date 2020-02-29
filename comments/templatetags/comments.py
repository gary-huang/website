from django import template
from comments import models as mods, forms

register = template.Library()


@register.simple_tag
def comments_for(id):
    comments = mods.Comment.objects.filter(thread_id="id").order_by("-created_at")


@register.inclusion_tag("comments_list.html", takes_context=True)
def render_comments_list_for(context, thread_id):
    all_comments = mods.Comment.objects.filter(thread_id=thread_id)
    parents = [(p, 0) for p in all_comments.filter(parent=None).order_by("created_at")]
    html = []
    last_indent = None
    while len(parents):
        p = parents.pop(0)
        if p == "end":
            html.append("end")
            continue

        p, indent = p
        html.append((p, indent))
        last_indent = indent
        parents = [(c, indent + 1) for c in p.children.order_by("created_at")] + ["end"] + parents

    html = [p[0] if isinstance(p, tuple) else p for p in html]
    form = forms.CommentForm()
    comments = mods.Comment.objects.filter(thread_id="id").order_by("created_at")
    return {
        "html": html,
        "thread_id": thread_id,
        "form": form,
        "user": context["user"],
    }


@register.inclusion_tag("comment_form.html", takes_context=True)
def render_comments_form(context, thread_id):
    form = models.PrayerRequestForm()
    return {
        "form": form
    }
