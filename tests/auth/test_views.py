from django.test import TestCase
from django.urls import reverse
from djplus.auth.forms import LoginForm


class LoginViewTest(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get(reverse("auth:login"))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_url_accessible_by_name(self):
        self.assertEqual(reverse("auth:login"), "/auth/login/")

    def test_use_correct_template(self):
        self.assertTemplateUsed(self.response, "auth/login.html")

    def test_login_form_exists_in_context(self):
        self.assertIn("form", self.response.context)
        self.assertIsInstance(self.response.context["form"], LoginForm)
