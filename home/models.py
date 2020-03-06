from django.db import models

from wagtail.core.models import Page

from church.models import ServicePage


class HomePage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        page = ServicePage.current_service_page()
        context["current_service_page"] = page
        return context
