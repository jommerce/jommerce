from django.shortcuts import render
from .forms import LoginForm


def login(request):
    form = LoginForm()
    context = {
        "form": form,
    }
    return render(request, "auth/login.html", context=context)


def logout(request):
    pass


def register(request):
    pass
