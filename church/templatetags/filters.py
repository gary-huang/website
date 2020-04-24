import arrow
from django import template

register = template.Library()


@register.filter(name="addclass")
def addclass(value, arg):
    return value.as_widget(attrs={"class": arg})


@register.filter(name="humandate")
def humandate(value):
    t = arrow.get(value).to("America/Toronto")
    return t.humanize()
