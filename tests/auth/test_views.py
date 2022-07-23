from django.test import TestCase, override_settings
from djplus.auth.models import User


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class LoginViewTests(TestCase):
    def test_template_name_for_login_page(self):
        response = self.client.get("/login/")
        self.assertTemplateUsed(response, "auth/login.html")


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class LogoutViewTests(TestCase):
    def test_template_name_for_logout_page(self):
        response = self.client.get("/logout/")
        self.assertTemplateUsed(response, "auth/logout.html")


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class SignupViewTests(TestCase):
    def test_template_name_for_signup_page(self):
        response = self.client.get("/signup/")
        self.assertTemplateUsed(response, "auth/signup.html")

    def test_sign_up_user_in_the_database(self):
        self.client.post("/signup/", data={"email": "staff@domain.com", "password": "password"})
        try:
            User.objects.get(email="staff@domain.com")
        except User.DoesNotExist:
            self.fail("The desired user is not saved in the database.")
