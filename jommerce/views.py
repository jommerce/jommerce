from django.views.generic import TemplateView
from django.shortcuts import render


class MaintenancePage(TemplateView):
    template_name = "maintenance.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, status=503)
