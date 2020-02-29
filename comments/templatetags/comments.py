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
        p, indent = parents.pop(0)
        if last_indent is not None:
            if last_indent < indent:
                for _ in range(last_indent, indent): html.append("in")
            elif last_indent > indent:
                for _ in range(indent, last_indent): html.append("out")

        html.append((p, indent))
        last_indent = indent
        parents = [(c, indent + 1) for c in p.children.order_by("created_at")] + parents

    # django templates don't support counting loops
    if html:
        last_indent = html[-1][1]
        for i in range(0, last_indent): html.append("out")

    html = [p[0] if isinstance(p, tuple) else p for p in html]
    form = forms.CommentForm()
    comments = mods.Comment.objects.filter(thread_id="id").order_by("created_at")
    return {
        "html": html,
        "thread_id": thread_id,
        "form": form
    }


@register.inclusion_tag("comment_form.html", takes_context=True)
def render_comments_form(context, thread_id):
    form = models.PrayerRequestForm()
    return {
        "form": form
    }
