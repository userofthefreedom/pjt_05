from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):

    interest_stocks = forms.MultipleChoiceField(
        choices=User.STOCK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

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

    def save(self, commit=True):
        user = super().save(commit=False)

        # 리스트 → 문자열 저장
        stocks = self.cleaned_data.get("interest_stocks")
        user.interest_stocks = ",".join(stocks)

        if commit:
            user.save()
        return user