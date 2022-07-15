from django.test import TestCase, override_settings, modify_settings
from djplus.auth.models import User


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class RedirectAfterLogin(TestCase):
    """ AUTH_LOGIN_REDIRECT_URL setting """

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test", password="123456")

    def setUp(self) -> None:
        self.response = self.client.post("/login/", data={"username": "test", "password": "123456"})

    @override_settings(AUTH_LOGIN_REDIRECT_URL="/custom/")
    def test_redirect_to_a_custom_url(self):
        self.assertRedirects(self.response, "/custom/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGIN_REDIRECT_URL="/")
    def test_redirect_to_home_page(self):
        self.assertRedirects(self.response, "/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGIN_REDIRECT_URL=None)
    def test_not_redirect(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "auth/login.html")


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class RedirectAfterLogout(TestCase):
    """ AUTH_LOGOUT_REDIRECT_URL setting """

    def setUp(self) -> None:
        self.response = self.client.post("/logout/")

    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/custom/")
    def test_redirect_to_a_custom_url(self):
        self.assertRedirects(self.response, "/custom/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/")
    def test_redirect_to_home_page(self):
        self.assertRedirects(self.response, "/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL=None)
    def test_not_redirect(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "auth/logout.html")


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class RedirectAfterSignup(TestCase):
    """ AUTH_SIGNUP_REDIRECT_URL setting """

    def setUp(self) -> None:
        self.response = self.client.post("/signup/", data={"username": "test", "password": "123456"})

    @override_settings(AUTH_SIGNUP_REDIRECT_URL="/custom/")
    def test_redirect_to_a_custom_url(self):
        self.assertRedirects(self.response, "/custom/", fetch_redirect_response=False)

    @override_settings(AUTH_SIGNUP_REDIRECT_URL="/")
    def test_redirect_to_home_page(self):
        self.assertRedirects(self.response, "/", fetch_redirect_response=False)

    @override_settings(AUTH_SIGNUP_REDIRECT_URL=None)
    def test_not_redirect(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "auth/signup.html")


@override_settings(ROOT_URLCONF="djplus.auth.urls")
@modify_settings(MIDDLEWARE={"append": "djplus.auth.middleware.AuthenticationMiddleware"})
class AccessLoginPageWhenUserIsAuthenticated(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test", password="123456")

    def setUp(self) -> None:
        self.client.post("/login/", data={"username": "test", "password": "123456"})
        self.response = self.client.get("/login/")

    @override_settings(AUTH_LOGIN_REDIRECT_URL="/custom/")
    def test_redirect_to_a_custom_url(self):
        self.assertRedirects(self.response, "/custom/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGIN_REDIRECT_URL="/")
    def test_redirect_to_home_page(self):
        self.assertRedirects(self.response, "/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGIN_REDIRECT_URL=None)
    def test_not_redirect(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "auth/login.html")


@override_settings(ROOT_URLCONF="djplus.auth.urls")
@modify_settings(MIDDLEWARE={"append": "djplus.auth.middleware.AuthenticationMiddleware"})
class AccessLoginPageWhenUserIsAnonymous(TestCase):
    def setUp(self) -> None:
        self.client.post("/logout/")
        self.response = self.client.get("/login/")

    def test_use_login_template(self):
        self.assertTemplateUsed(self.response, "auth/login.html")

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    @override_settings(AUTH_LOGIN_REDIRECT_URL="/custom/")
    def test_no_redirect(self):
        self.assertNotEqual(self.response.status_code, 302)


@override_settings(ROOT_URLCONF="djplus.auth.urls")
@modify_settings(MIDDLEWARE={"append": "djplus.auth.middleware.AuthenticationMiddleware"})
class AccessSignupPageWhenUserIsAuthenticated(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test", password="123456")

    def setUp(self) -> None:
        self.client.post("/login/", data={"username": "test", "password": "123456"})
        self.response = self.client.get("/signup/")

    @override_settings(AUTH_SIGNUP_REDIRECT_URL="/custom/")
    def test_redirect_to_a_custom_url(self):
        self.assertRedirects(self.response, "/custom/", fetch_redirect_response=False)

    @override_settings(AUTH_SIGNUP_REDIRECT_URL="/")
    def test_redirect_to_home_page(self):
        self.assertRedirects(self.response, "/", fetch_redirect_response=False)

    @override_settings(AUTH_SIGNUP_REDIRECT_URL=None)
    def test_no_redirect(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "auth/signup.html")


@override_settings(ROOT_URLCONF="djplus.auth.urls")
@modify_settings(MIDDLEWARE={"append": "djplus.auth.middleware.AuthenticationMiddleware"})
class AccessSignupPageWhenUserIsAnonymous(TestCase):
    def setUp(self) -> None:
        self.client.post("/logout/")
        self.response = self.client.get("/signup/")

    def test_use_signup_template(self):
        self.assertTemplateUsed(self.response, "auth/signup.html")

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    @override_settings(AUTH_SIGNUP_REDIRECT_URL="/custom/")
    def test_no_redirect(self):
        self.assertNotEqual(self.response.status_code, 302)


@override_settings(ROOT_URLCONF="djplus.auth.urls")
@modify_settings(MIDDLEWARE={"append": "djplus.auth.middleware.AuthenticationMiddleware"})
class AccessLogoutPageWhenUserIsAuthenticated(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test", password="123456")

    def setUp(self) -> None:
        self.client.post("/login/", data={"username": "test", "password": "123456"})
        self.response = self.client.get("/logout/")

    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/custom/")
    def test_redirect_to_a_custom_url(self):
        self.assertRedirects(self.response, "/custom/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/")
    def test_redirect_to_home_page(self):
        self.assertRedirects(self.response, "/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL=None)
    def test_no_redirect(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "auth/logout.html")


@override_settings(ROOT_URLCONF="djplus.auth.urls")
@modify_settings(MIDDLEWARE={"append": "djplus.auth.middleware.AuthenticationMiddleware"})
class AccessLogoutPageWhenUserIsAnonymous(TestCase):
    def setUp(self) -> None:
        self.client.post("/logout/")
        self.response = self.client.get("/logout/")

    def test_do_not_use_logout_template(self):
        self.assertTemplateNotUsed(self.response, "auth/logout.html")

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 302)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/custom/")
    def test_redirect_to_a_custom_url(self):
        self.assertRedirects(self.response, "/custom/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL="/")
    def test_redirect_to_home_page(self):
        self.assertRedirects(self.response, "/", fetch_redirect_response=False)

    @override_settings(AUTH_LOGOUT_REDIRECT_URL=None)
    def test_redirect_to_home_page_by_default(self):
        self.assertRedirects(self.response, "/", fetch_redirect_response=False)
