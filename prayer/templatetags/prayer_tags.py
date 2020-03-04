from django import template

from prayer import forms, models
from utils import views as viewtils


register = template.Library()


@register.inclusion_tag("prayer_requests.html", takes_context=True)
def user_prayer_requests(context, req_user):
    user = context.request.user
    if not user.is_authenticated or user != req_user:
        raise exceptions.PermissionDenied("")
    context["prayer_requests"] = models.PrayerRequest.for_user(user)
    return context


@register.inclusion_tag("prayer_requests.html", takes_context=True)
def prayer_requests(context):
    user = context.request.user

    if not user.is_authenticated:
        raise exceptions.PermissionDenied("")

    context["prayer_requests"] = models.PrayerRequest.crossroads_requests_for_user(user)
    return context


@register.inclusion_tag("prayer_form.html")
def prayer_request_form():
    return { "form": forms.PrayerRequestForm() }


@register.inclusion_tag("public_prayer_form.html")
def public_prayer_request_form():
    return { "form": forms.PrayerRequestForm() }


@viewtils.authenticated
def delete_prayer_request(request, id):
    preq = models.PrayerRequest.objects.get(pk=id)
    if preq.user != request.user:
        raise exceptions.PermissionDenied("")
    preq.delete()
    return http.HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#prayer-requests")
