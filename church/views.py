import functools

from django import http, shortcuts
from django.core import exceptions
from django.urls import reverse

from church import models
from church.templatetags.prayer_tags import register


def authenticated(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        context = args[0]
        if hasattr(context, "user"):
            user = context.user
        elif hasattr(context, "request") and hasattr(context.request, "user"):
            user = context.request.user
        else:
            raise exceptions.PermissionDenied("")

        if not user.is_authenticated:
            raise exceptions.PermissionDenied("")
        return f(*args, **kwargs)
    return wrapper


@register.inclusion_tag("prayer_requests.html", takes_context=True)
def user_prayer_requests(context, req_user):
    # TODO: this should permit a user seeing another user's prayer items
    #       that they're permitted to
    user = context.request.user
    if not user.is_authenticated or user != req_user:
        raise exceptions.PermissionDenied("")
    prayer_requests = models.PrayerRequest.objects.filter(user=user)
    context["prayer_requests"] = prayer_requests
    return context


@register.inclusion_tag("prayer_requests.html", takes_context=True)
def prayer_requests(context):
    user = context.request.user

    if not user.is_authenticated:
        raise exceptions.PermissionDenied("")

    prayer_requests = models.PrayerRequest.objects.filter(post_visibility="4")

    user = context.request.user
    if user.is_authenticated:
        prayer_requests |= models.PrayerRequest.objects.filter(user=user)
    user_groups = [group.name for group in user.groups.all()]
    if "member" in user_groups:
        prayer_requests |= models.PrayerRequest.objects.filter(post_visibility="2")
    if "prayer_team" in user_groups:
        prayer_requests |= models.PrayerRequest.objects.filter(post_visibility="3")

    context["prayer_requests"] = prayer_requests
    return context


@register.inclusion_tag("prayer_form.html")
def prayer_request_form():
    return { "form": models.PrayerRequestForm() }


@register.inclusion_tag("public_prayer_form.html")
def public_prayer_request_form():
    return { "form": models.PrayerRequestForm() }


def submit_prayer_form(request):
    if not request.user.is_authenticated:
        raise exceptions.PermissionDenied("")

    if request.method == "POST":
        form = models.PrayerRequestForm(request.POST)

        if form.is_valid():
            models.PrayerRequest.objects.create(
                user=request.user,
                user_visibility=int(form.cleaned_data["user_visibility"]),
                post_visibility=int(form.cleaned_data["post_visibility"]),
                body=form.cleaned_data["body"]
            )
            return http.HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#prayer-requests")

    else:
        form = models.PrayerRequestForm()

    return shortcuts.render(request, "prayer_form.html", { "form": form })


@authenticated
def delete_prayer_request(request, id):
    preq = models.PrayerRequest.objects.get(pk=id)
    if preq.user != request.user:
        raise exceptions.PermissionDenied("")
    preq.delete()
    return http.HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#prayer-requests")


def profile(request):
    if not request.user.is_authenticated:
        return http.HttpResponseRedirect(reverse("login"))
    return shortcuts.render(request, "profile.html", {
    })
