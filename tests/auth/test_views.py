from django.test import TestCase, override_settings
from djplus.auth.models import User, AnonymousUser, Session
from djplus.auth import forms


class AuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = User(email="test@example.com", password="123456")
        request.session = Session()
        return self.get_response(request)


class AnonymousUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = AnonymousUser()
        request.session = Session()
        return self.get_response(request)


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class LoginViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email="test@example.com", password="123456")

    @override_settings(AUTH_SESSION_COOKIE_NAME="session_id")
    @override_settings(MIDDLEWARE=["djplus.auth.middleware.AuthenticationMiddleware"])
    def test_Login_successfully(self):
        response = self.client.post("/login/", data={"email": "test@example.com", "password": "123456"})
        self.assertIn("session_id", response.cookies)
        session = Session.objects.get(pk=response.cookies["session_id"].value)
        self.assertEqual(session.user, self.user)

    @override_settings(AUTH_LOGIN_REDIRECT_URL="/custom/")
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AnonymousUserMiddleware"])
    def test_redirect_after_login(self):
        response = self.client.post("/login/", data={"email": "test@example.com", "password": "123456"})
        self.assertRedirects(response, "/custom/", fetch_redirect_response=False)

    def test_get_login_page_as_anonymous_user(self):
        response = self.client.get("/login/")
        self.assertTemplateUsed(response, "auth/login.html")
        self.assertEqual(response.status_code, 200)

    @override_settings(AUTH_LOGIN_REDIRECT_URL="/test/")
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AuthenticatedUserMiddleware"])
    def test_get_login_page_as_authenticated_user(self):
        response = self.client.get("/login/")
        self.assertRedirects(response, "/test/", fetch_redirect_response=False)

    def test_form_on_the_login_page(self):
        response = self.client.get("/login/")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], forms.LoginForm)

    def test_login_with_an_email_that_does_not_exist(self):
        response = self.client.post("/login/", data={"email": "fake@example.com", "password": "123456"})
        self.assertFormError(response, "form", "email", ["This email does not exist."])

    def test_login_with_wrong_password(self):
        response = self.client.post("/login/", data={"email": "test@example.com", "password": "111111"})
        self.assertFormError(response, "form", "password", ["Incorrect password"])


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class LogoutViewTests(TestCase):
    @override_settings(AUTH_SESSION_COOKIE_NAME="session_key")
    @override_settings(MIDDLEWARE=["djplus.auth.middleware.AuthenticationMiddleware"])
    def test_logout_successfully(self):
        User.objects.create(email="test@example.com", password="123456")
        self.client.post("/login/", data={"email": "test@example.com", "password": "123456"})
        response = self.client.post("/logout/")
        self.assertNotIn("session_key", response.cookies)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/custom/")
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AuthenticatedUserMiddleware"])
    def test_redirect_after_logout(self):
        response = self.client.post("/logout/")
        self.assertRedirects(response, "/custom/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/test/")
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AnonymousUserMiddleware"])
    def test_get_logout_page_as_anonymous_user(self):
        response = self.client.get("/logout/")
        self.assertRedirects(response, "/test/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/goodbye/")
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AuthenticatedUserMiddleware"])
    def test_get_logout_page_as_authenticated_user(self):
        response = self.client.get("/logout/")
        self.assertRedirects(response, "/goodbye/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL=None)
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AuthenticatedUserMiddleware"])
    def test_get_logout_page_as_authenticated_user_when_logout_redirect_url_setting_is_none(self):
        response = self.client.get("/logout/")
        self.assertTemplateUsed(response, "auth/logout.html")
        self.assertEqual(response.status_code, 200)


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class SignupViewTests(TestCase):
    def test_signup_successfully(self):
        self.client.post("/signup/", data={"email": "staff@domain.com", "password": "password"})
        try:
            User.objects.get(email="staff@domain.com")
        except User.DoesNotExist:
            self.fail("Registration failed.")

    @override_settings(AUTH_SIGNUP_REDIRECT_URL="/custom/")
    def test_redirect_after_signup(self):
        response = self.client.post("/signup/", data={"email": "staff@domain.com", "password": "password"})
        self.assertRedirects(response, "/custom/", fetch_redirect_response=False)

    def test_get_signup_page_as_anonymous_user(self):
        response = self.client.get("/signup/")
        self.assertTemplateUsed(response, "auth/signup.html")
        self.assertEqual(response.status_code, 200)

    @override_settings(AUTH_SIGNUP_REDIRECT_URL="/test/")
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AuthenticatedUserMiddleware"])
    def test_get_signup_page_as_authenticated_user(self):
        response = self.client.get("/signup/")
        self.assertRedirects(response, "/test/", fetch_redirect_response=False)

    def test_form_on_the_signup_page(self):
        response = self.client.get("/signup/")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], forms.SignupForm)

    def test_signup_with_an_existing_email(self):
        User.objects.create(email="test@example.com", password="123456")
        response = self.client.post("/signup/", data={"email": "test@example.com", "password": "123456"})
        self.assertFormError(response, "form", "email", ["This email already exists."])
