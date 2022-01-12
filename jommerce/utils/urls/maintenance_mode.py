from django.urls import path, re_path
from django.contrib import admin
from django.shortcuts import render

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path("", lambda request: render(request, "503.html", status=503)),
]
