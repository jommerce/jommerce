from django.urls import path
from .views import index, PostDetailView

app_name = "blog"

urlpatterns = [
    path("", index, name="index"),
    path("<slug>/", PostDetailView.as_view(), name="post"),
]
