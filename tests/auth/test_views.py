from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from djplus.auth.forms import LoginForm
from djplus.auth.models import User


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class LoginViewTest(TestCase):
    user_data = {
        "username": "test",
        "password": "123456",
    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create(**cls.user_data)

    def setUp(self) -> None:
        self.client.post("/logout/")

    def test_login_redirect_url_setting(self):
        for url in {"/custom/", "/"}:
            with self.subTest(AUTH_LOGIN_REDIRECT_URL=url), self.settings(AUTH_LOGIN_REDIRECT_URL=url):
                response = self.client.post("/login/", data=self.user_data)
                self.assertRedirects(response, url, fetch_redirect_response=False)


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class LogoutViewTest(TestCase):
    user_data = {
        "username": "test",
        "password": "123456",
    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create(**cls.user_data)

    def login(self):
        self.client.post("/login/", data=self.user_data)

    @override_settings(AUTH_SESSION_COOKIE_NAME="custom")
    def test_logout_with_custom_session_cookie_name(self):
        response = self.client.post("/logout/")
        self.assertNotIn("custom", response.cookies)

    def test_logout_redirect_url_setting(self):
        for url in {"/custom/", "/"}:
            with self.subTest(AUTH_LOGOUT_REDIRECT_URL=url), self.settings(AUTH_LOGOUT_REDIRECT_URL=url):
                self.login()
                response = self.client.post("/logout/")
                self.assertRedirects(response, url, fetch_redirect_response=False)

        with self.subTest(AUTH_LOGOUT_REDIRECT_URL=None), self.settings(AUTH_LOGOUT_REDIRECT_URL=None):
            self.login()
            response = self.client.post("/logout/")
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "auth/logout.html")
