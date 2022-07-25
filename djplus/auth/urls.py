from django.urls import path
from .views import login, logout, signup

app_name = "auth"

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("signup/", signup, name="signup"),
]
