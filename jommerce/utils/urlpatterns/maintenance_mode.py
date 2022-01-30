from django.urls import re_path
from django.shortcuts import render

urlpatterns = [
    re_path("", lambda request: render(request, "503.html", status=503)),
]
