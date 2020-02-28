from django import forms

from wagtail.users import wtforms


class UserEditForm(wtforms.UserEditForm):
    pass


class CustomUserCreationForm(wtforms.UserCreationForm):
    pass
