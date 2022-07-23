from django.test import TestCase, override_settings


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class LoginViewTests(TestCase):
    def test_template_name_for_login_page(self):
        response = self.client.get("/login/")
        self.assertTemplateUsed(response, "auth/login.html")
