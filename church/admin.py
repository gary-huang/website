from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

from . import email


def email_bulletin(modeladmin, request, queryset):
    try:
        email.send_bulletin(queryset)
    except Exception as e:
        print(e)
        messages.error(request, f"Error: {e}")
    else:
        messages.success(request, f"{len(queryset)} email(s) sent successfully!")


def service_email(modeladmin, request, queryset):
    try:
        email.send_service(queryset)
    except Exception as e:
        print(e)
        messages.error(request, f"Error: {e}")
    else:
        messages.success(request, f"{len(queryset)} email(s) sent successfully!")


class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Authentication", dict(fields=("token",),)),
    )
    actions = [email_bulletin, service_email]


admin.site.register(User, UserAdmin)
