from django import forms

from wagtail.users import forms as wtforms


class UserEditForm(wtforms.UserEditForm):
    pass


class CustomUserCreationForm(wtforms.UserCreationForm):
    pass
