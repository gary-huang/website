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


class UserAdmin(DjangoUserAdmin):
    actions = [email_bulletin]


admin.site.register(User, UserAdmin)
