from django.shortcuts import render, redirect
from .forms import SignupForm


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = SignupForm()

    context = {
        "form": form,
    }

    return render(request, "accounts/signup.html", context)


def login_view(request):
    pass