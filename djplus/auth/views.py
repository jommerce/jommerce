from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.conf import settings
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
                return redirect(settings.AUTH_LOGIN_REDIRECT_URL)
            else:
                form.add_error("password", _("Incorrect password"))
    return render(request, "auth/login.html", context={"form": form})


def logout(request):
    if hasattr(request, "user"):
        if settings.AUTH_LOGOUT_REDIRECT_URL:
            return redirect(settings.AUTH_LOGOUT_REDIRECT_URL)
    if request.method == "POST":
        return redirect(settings.AUTH_LOGOUT_REDIRECT_URL)
    return render(request, "auth/logout.html")


def signup(request):
    if hasattr(request, "user") and request.user.is_authenticated:
        return redirect(settings.AUTH_SIGNUP_REDIRECT_URL)
    if request.method == "POST":
        User.objects.create(email=request.POST["email"], password=request.POST["password"])
        return redirect(settings.AUTH_SIGNUP_REDIRECT_URL)
    return render(request, "auth/signup.html", context={"form": SignupForm()})
