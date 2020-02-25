from django import http, shortcuts

from church import models
from church.templatetags.prayer_tags import register


@register.inclusion_tag("prayer_requests.html", takes_context=True)
def prayer_requests(context):
    prayer_requests = []

    if context.request.user.is_authenticated:
        pass

    return {
        "prayer_requests": [
            {"value": "please pray for students with midterms upcoming", "user": "Anonymous"},
        ]
    }


@register.inclusion_tag("prayer_form.html")
def prayer_request_form():
    return { "form": models.PrayerRequestForm() }


def submit_prayer_form(request):
    if request.method == "POST":
        form = models.PrayerRequestForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data["prayer_request"])
            return http.HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    else:
        form = models.PrayerRequestForm()

    return shortcuts.render(request, "prayer_form.html", { "form": form })
