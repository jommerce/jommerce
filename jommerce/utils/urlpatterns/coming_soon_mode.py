from django.views.generic import TemplateView
from django.urls import re_path

urlpatterns = [
    re_path("", TemplateView.as_view(template_name="coming-soon.html")),
]
