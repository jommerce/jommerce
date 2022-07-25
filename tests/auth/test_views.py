from django.test import TestCase, override_settings
from djplus.auth.models import User, AnonymousUser
from djplus.auth import forms


class AuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = User(email="test@example.com", password="123456")
        return self.get_response(request)


class AnonymousUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = AnonymousUser()
        return self.get_response(request)


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

    @override_settings(AUTH_LOGIN_REDIRECT_URL="/test/")
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AuthenticatedUserMiddleware"])
    def test_redirect_authenticated_user_to_custom_page_when_accessing_login_page(self):
        response = self.client.get("/login/")
        self.assertRedirects(response, "/test/", fetch_redirect_response=False)

    def test_login_form(self):
        response = self.client.get("/login/")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], forms.LoginForm)

    def test_log_in_a_user_that_does_not_exist_in_the_database(self):
        response = self.client.post("/login/", data={"email": "fake@example.com", "password": "123456"})
        self.assertFormError(response, "form", "email", ["This email does not exist."])


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class LogoutViewTests(TestCase):
    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/goodbye/")
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AuthenticatedUserMiddleware"])
    def test_redirect_authenticated_user_when_accessing_logout_page(self):
        response = self.client.get("/logout/")
        self.assertRedirects(response, "/goodbye/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/custom/")
    def test_redirect_user_to_custom_page_after_successfully_log_out(self):
        response = self.client.post("/logout/")
        self.assertRedirects(response, "/custom/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/test/")
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AnonymousUserMiddleware"])
    def test_redirect_anonymous_user_when_accessing_logout_page(self):
        response = self.client.get("/logout/")
        self.assertRedirects(response, "/test/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL=None)
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AuthenticatedUserMiddleware"])
    def test_template_name_when_authenticated_user_get_logout_page(self):
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

    @override_settings(AUTH_SIGNUP_REDIRECT_URL="/test/")
    @override_settings(MIDDLEWARE=["tests.auth.test_views.AuthenticatedUserMiddleware"])
    def test_redirect_authenticated_user_to_custom_page_when_accessing_signup_page(self):
        response = self.client.get("/signup/")
        self.assertRedirects(response, "/test/", fetch_redirect_response=False)

    def test_signup_form(self):
        response = self.client.get("/signup/")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], forms.SignupForm)
