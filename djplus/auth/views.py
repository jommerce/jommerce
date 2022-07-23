from django.shortcuts import render


def login(request):
    return render(request, "auth/login.html")


def logout(request):
    pass


def signup(request):
    pass
