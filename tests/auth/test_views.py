from django.test import TestCase, override_settings
from djplus.auth.models import User


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class LoginViewTests(TestCase):
    def test_template_name_for_login_page(self):
        response = self.client.get("/login/")
        self.assertTemplateUsed(response, "auth/login.html")

    @override_settings(AUTH_LOGIN_REDIRECT_URL="/custom/")
    def test_redirect_user_to_custom_page_after_successfully_log_in(self):
        User.objects.create(email="test@example.com", password="123456")
        response = self.client.post("/login/", data={"email": "test@example.com", "password": "123456"})
        self.assertRedirects(response, "/custom/", fetch_redirect_response=False)


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

    @override_settings(AUTH_SIGNUP_REDIRECT_URL="/custom/")
    def test_redirect_user_to_custom_page_after_successfully_sign_up(self):
        response = self.client.post("/signup/", data={"email": "staff@domain.com", "password": "password"})
        self.assertRedirects(response, "/custom/", fetch_redirect_response=False)
