from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = SignupForm()

    context = {
        "form": form,
    }

    return render(request, "accounts/signup.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()

    context = {
        "form": form,
    }

    return render(request, "accounts/login.html", context)


def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("/")