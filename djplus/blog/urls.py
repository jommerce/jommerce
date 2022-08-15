from django.urls import path
from .views import index, PostDetailView


urlpatterns = [
    path("", index, name="index"),
    path("<slug>/", PostDetailView.as_view(), name="post"),
]
