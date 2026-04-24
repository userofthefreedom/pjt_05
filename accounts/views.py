from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import SignupForm
from django.contrib.auth.decorators import login_required


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

    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if next_url:
                return redirect(next_url)

            return redirect("/")
    else:
        form = AuthenticationForm()

    context = {
        "form": form,
        "next": next_url,
    }

    return render(request, "accounts/login.html", context)


def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("/")


@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            # 비밀번호 변경 후에도 현재 로그인 세션을 유지한다.
            update_session_auth_hash(request, user)

            return redirect("accounts:password_change_done")
    else:
        form = PasswordChangeForm(request.user)

    context = {
        "form": form,
    }

    return render(request, "accounts/password_change.html", context)


@login_required
def password_change_done(request):
    return render(request, "accounts/password_change_done.html")