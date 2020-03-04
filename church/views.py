import functools

from django import http, shortcuts
from django.core import exceptions
from django.urls import reverse

from church import models


def profile(request):
    if not request.user.is_authenticated:
        return http.HttpResponseRedirect(reverse("login"))
    return shortcuts.render(request, "profile.html", {
    })
