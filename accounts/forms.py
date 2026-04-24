from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    nickname = forms.CharField(max_length=50)
    interest_stocks = forms.CharField(max_length=255, required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "nickname",
            "interest_stocks",
            "profile_image",
        )