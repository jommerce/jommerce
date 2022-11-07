from django.urls import path, include
from django.conf import settings

urlpatterns = [

]

if "django.contrib.admin" in settings.INSTALLED_APPS:
    from django.contrib import admin
    urlpatterns += [path("admin/", admin.site.urls)]

if "djplus.auth" in settings.INSTALLED_APPS:
    urlpatterns += [path("auth/", include("djplus.auth.urls", namespace="auth"))]

if "djplus.blog" in settings.INSTALLED_APPS:
    urlpatterns += [path("blog/", include("djplus.blog.urls", namespace="blog"))]

if "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls", namespace="djdt"))]
