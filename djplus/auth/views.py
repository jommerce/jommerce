from django.views.generic import FormView
from .forms import LoginForm


class LoginView(FormView):
    template_name = "auth/login.html"
    form_class = LoginForm
