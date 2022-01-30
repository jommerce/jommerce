from django.views.generic import TemplateView
from django.urls import path, re_path
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path("", TemplateView.as_view(template_name="coming-soon.html")),
]
