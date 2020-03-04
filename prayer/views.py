from django import http, shortcuts

from prayer import forms, models
from utils import views as viewtils


@viewtils.authenticated
def delete_prayer_request(request, id):
    pr = models.PrayerRequest.objects.get(pk=id)
    if pr.author != request.user:
        raise exceptions.PermissionDenied("")
    pr.delete()
    return http.HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#prayer-requests")


def submit_prayer_form(request):
    if not request.user.is_authenticated:
        raise exceptions.PermissionDenied("")

    if request.method == "POST":
        form = forms.PrayerRequestForm(request.POST)

        if form.is_valid():
            models.PrayerRequest.objects.create(
                author=request.user,
                body_visibility=form.cleaned_data["body_visibility"],
                body=form.cleaned_data["body"],
                provided_name=form.cleaned_data["provided_name"],
            )
            return http.HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#prayer-requests")

    else:
        form = forms.PrayerRequestForm()

    return shortcuts.render(request, "prayer_form.html", { "form": form })


@viewtils.authenticated
def prayer_request_react(request, pr_id, emoji):
    pr = models.PrayerRequest.objects.get(pk=pr_id)
    existing_reacts = models.PrayerRequestReact.objects.filter(item=pr, type=emoji, user=request.user)
    if len(existing_reacts):
        for r in existing_reacts:
            r.delete()
        return http.HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#prayer-requests")
    react = models.PrayerRequestReact.objects.create(item=pr, type=emoji, user=request.user)
    return http.HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#prayer-requests")
