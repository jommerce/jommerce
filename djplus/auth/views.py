from django.shortcuts import render, redirect
from django.conf import settings
from .models import User


def login(request):
    return render(request, "auth/login.html")


def logout(request):
    return render(request, "auth/logout.html")


def signup(request):
    if request.method == "POST":
        User.objects.create(email=request.POST["email"], password=request.POST["password"])
        return redirect(settings.AUTH_SIGNUP_REDIRECT_URL)
    return render(request, "auth/signup.html")
