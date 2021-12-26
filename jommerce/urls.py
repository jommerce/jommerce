from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from .views import MaintenancePage

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if getattr(settings, "MAINTENANCE_MODE", False):
    urlpatterns = [
        path("admin/", admin.site.urls),
        re_path("", MaintenancePage.as_view()),
    ]

if getattr(settings, "COMING_SOON_MODE", False):
    urlpatterns = [
        path("admin/", admin.site.urls),
        re_path("", TemplateView.as_view(template_name="coming-soon.html")),
    ]

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
