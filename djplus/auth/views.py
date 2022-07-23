from django.shortcuts import render


def login(request):
    return render(request, "auth/login.html")


def logout(request):
    return render(request, "auth/logout.html")


def signup(request):
    return render(request, "auth/signup.html")
