import functools

from django import http, shortcuts
from django.core import exceptions
from django.urls import reverse

from church import models
from prayer import models as pr_models
from utils import views as viewtils


def profile(request):
    if not request.user.is_authenticated:
        return http.HttpResponseRedirect(reverse("login"))
    return shortcuts.render(request, "profile.html", {
    })


@viewtils.authenticated
def add_pr_to_next_service(request, pr_id):
    pr = pr_models.PrayerRequest.get_for_user(pr_id, request.user)

    # sp = models.ServicePage.next_service_page()
    sp = models.ServicePage.current_service_page()
    sp.prayer_requests.add(pr)
    return http.HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@viewtils.authenticated
def rm_pr_from_service(request, pr_id, sp_id):
    pr = pr_models.PrayerRequest.get_for_user(pr_id, request.user)
    sp = models.ServicePage.objects.get(pk=sp_id)
    sp.prayer_requests.remove(pr)
    return http.HttpResponseRedirect(request.META.get("HTTP_REFERER"))
