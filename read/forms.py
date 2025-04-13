from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

