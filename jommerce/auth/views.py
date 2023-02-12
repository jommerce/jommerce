from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from .conf import settings
from .forms import LoginForm, SignupForm
from .models import User


def login(request):
    form = LoginForm(request.POST or None)
    if hasattr(request, "user") and request.user.is_authenticated:
        return redirect(settings.AUTH_LOGIN_REDIRECT_URL)
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST["email"])
        except User.DoesNotExist:
            form.add_error("email", _("This email does not exist."))
        else:
            if user.verify_password(request.POST["password"]):
                request.session.user = user
                return redirect(settings.AUTH_LOGIN_REDIRECT_URL)
            else:
                form.add_error("password", _("Incorrect password"))
    return render(request, "auth/login.html", context={"form": form})


def logout(request):
    if hasattr(request, "user") or request.method == "POST":
        if settings.AUTH_LOGOUT_REDIRECT_URL:
            request.session.user = None
            return redirect(settings.AUTH_LOGOUT_REDIRECT_URL)
        else:
            if request.user.is_anonymous:
                return redirect(settings.AUTH_LOGIN_URL)
    request.session.user = None
    return render(request, "auth/logout.html")


def signup(request):
    form = SignupForm(request.POST or None)
    if hasattr(request, "user") and request.user.is_authenticated:
        return redirect(settings.AUTH_SIGNUP_REDIRECT_URL)
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST["email"])
        except User.DoesNotExist:
            User.objects.create(
                email=request.POST["email"], password=request.POST["password"]
            )
            return redirect(settings.AUTH_SIGNUP_REDIRECT_URL)
        else:
            form.add_error("email", _("This email already exists."))
    return render(request, "auth/signup.html", context={"form": form})
