import functools

from django import http, shortcuts
from django.core import exceptions

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
def prayer_requests(context):
    prayer_requests = models.PrayerRequest.objects.filter(post_visibility="4")

    user = context.request.user
    if user.is_authenticated:
        prayer_requests |= models.PrayerRequest.objects.filter(user=user)
    user_groups = [group.name for group in user.groups.all()]
    if "member" in user_groups:
        prayer_requests |= models.PrayerRequest.objects.filter(post_visibility="2")
    if "prayer_team" in user_groups:
        prayer_requests |= models.PrayerRequest.objects.filter(post_visibility="3")

    pr_data = []
    for pr in prayer_requests:
        if pr.user_visibility == "4" or \
           pr.user_visibility == "3" and "prayer_team" in user_groups or \
           pr.user_visibility == "2" and "member" in user_groups or \
           pr.user == user:
            username = pr.user.username
        else:
            username = "Anonymous"

        pr_data.append({
            "id": pr.pk,
            "value": pr.body,
            "user": pr.user.username,
        })


    return {
        "prayer_requests": pr_data,
        "user": user,
    }


@register.inclusion_tag("prayer_form.html")
def prayer_request_form():
    return { "form": models.PrayerRequestForm() }


def submit_prayer_form(request):
    if not request.user.is_authenticated:
        raise PermissionDenied()

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
