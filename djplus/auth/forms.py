from django import forms
from .models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "password")


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "password")
