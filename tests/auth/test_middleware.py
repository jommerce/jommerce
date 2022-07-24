from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from django.conf import settings
from djplus.auth.middleware import AuthenticationMiddleware, AnonymousUser
from djplus.auth.models import User, Session

SESSION_COOKIE_NAME = settings.AUTH_SESSION_COOKIE_NAME


class AuthenticationMiddlewareTests(TestCase):
    def setUp(self) -> None:
        self.request = RequestFactory().get("/")
        self.middleware = AuthenticationMiddleware(lambda req: HttpResponse())

    def test_existence_of_user_attribute(self):
        self.middleware(self.request)
        self.assertTrue(hasattr(self.request, "user"))
        self.assertTrue(isinstance(self.request.user, (User, AnonymousUser)))

    def test_existence_of_session_attribute(self):
        self.middleware(self.request)
        self.assertTrue(hasattr(self.request, "session"))
        self.assertIsInstance(self.request.session, Session)

    def test_identify_an_anonymous_user_who_does_not_have_a_session(self):
        self.middleware(self.request)
        self.assertIsInstance(self.request.user, AnonymousUser)
        self.assertIsNone(self.request.session.user)

    def test_identify_an_anonymous_user_whose_session_is_empty(self):
        self.request.COOKIES[SESSION_COOKIE_NAME] = ""
        self.middleware(self.request)
        self.assertIsInstance(self.request.user, AnonymousUser)
        self.assertIsNone(self.request.session.user)

    def test_identify_an_anonymous_user_whose_session_does_exist_in_the_database(self):
        Session.objects.create(id="anonymous_session")

        self.request.COOKIES[SESSION_COOKIE_NAME] = "anonymous_session"
        self.middleware(self.request)
        self.assertIsInstance(self.request.user, AnonymousUser)
        self.assertIsNone(self.request.session.user)

    def test_identify_an_anonymous_user_whose_session_does_not_exist_in_the_database(self):
        self.request.COOKIES[SESSION_COOKIE_NAME] = "fake_session"
        self.middleware(self.request)
        self.assertIsInstance(self.request.user, AnonymousUser)
        self.assertIsNone(self.request.session.user)

    def test_identify_authenticated_user_whose_session_exists_in_the_database(self):
        user = User.objects.create(email="test@example.com", password="123456")
        session = Session.objects.create(id="user_session", user=user)

        self.request.COOKIES[SESSION_COOKIE_NAME] = "user_session"
        self.middleware(self.request)
        self.assertIsInstance(self.request.user, User)
        self.assertIsNotNone(self.request.session.user)
        self.assertEqual(self.request.user, user)
        self.assertEqual(self.request.session, session)
        self.assertEqual(self.request.session.user, user)

    def test_not_saving_empty_sessions(self):
        def view(request):
            request.session.save()
            return HttpResponse()
        middleware = AuthenticationMiddleware(view)
        middleware(self.request)
        try:
            Session.objects.get(id=self.request.session.id)
        except Session.DoesNotExist:
            pass
        else:
            self.fail("The desired session was created")

    def test_secure_session_cookie(self):
        with self.settings(AUTH_SESSION_COOKIE_SECURE=True):
            response = self.middleware(self.request)
            self.assertTrue(response.cookies[SESSION_COOKIE_NAME]["secure"])
        with self.settings(AUTH_SESSION_COOKIE_SECURE=False):
            response = self.middleware(self.request)
            self.assertFalse(response.cookies[SESSION_COOKIE_NAME]["secure"])

    def test_httponly_session_cookie(self):
        with self.settings(AUTH_SESSION_COOKIE_HTTPONLY=True):
            response = self.middleware(self.request)
            self.assertTrue(response.cookies[SESSION_COOKIE_NAME]["httponly"])
        with self.settings(AUTH_SESSION_COOKIE_HTTPONLY=False):
            response = self.middleware(self.request)
            self.assertFalse(response.cookies[SESSION_COOKIE_NAME]["httponly"])

    def test_samesite_session_cookie(self):
        with self.settings(AUTH_SESSION_COOKIE_SAMESITE="Strict"):
            response = self.middleware(self.request)
            self.assertEqual(response.cookies[SESSION_COOKIE_NAME]["samesite"], "Strict")
        with self.settings(AUTH_SESSION_COOKIE_SAMESITE="Lax"):
            response = self.middleware(self.request)
            self.assertEqual(response.cookies[SESSION_COOKIE_NAME]["samesite"], "Lax")
        with self.settings(AUTH_SESSION_COOKIE_SAMESITE="None"):
            response = self.middleware(self.request)
            self.assertEqual(response.cookies[SESSION_COOKIE_NAME]["samesite"], "None")
        with self.settings(AUTH_SESSION_COOKIE_SAMESITE=False):
            response = self.middleware(self.request)
            self.assertFalse(response.cookies[SESSION_COOKIE_NAME]["samesite"])

    def test_domain_session_cookie(self):
        with self.settings(AUTH_SESSION_COOKIE_DOMAIN=".example.com"):
            response = self.middleware(self.request)
            self.assertEqual(response.cookies[SESSION_COOKIE_NAME]["domain"], ".example.com")
        with self.settings(AUTH_SESSION_COOKIE_DOMAIN="example.local"):
            response = self.middleware(self.request)
            self.assertEqual(response.cookies[SESSION_COOKIE_NAME]["domain"], "example.local")
        with self.settings(AUTH_SESSION_COOKIE_DOMAIN=None):
            response = self.middleware(self.request)
            self.assertEqual(response.cookies[SESSION_COOKIE_NAME]["domain"], "")

    def test_path_session_cookie(self):
        with self.settings(AUTH_SESSION_COOKIE_PATH="/"):
            response = self.middleware(self.request)
            self.assertEqual(response.cookies[SESSION_COOKIE_NAME]["path"], "/")
        with self.settings(AUTH_SESSION_COOKIE_PATH="/custom/"):
            response = self.middleware(self.request)
            self.assertEqual(response.cookies[SESSION_COOKIE_NAME]["path"], "/custom/")
        with self.settings(AUTH_SESSION_COOKIE_PATH="/example/"):
            response = self.middleware(self.request)
            self.assertEqual(response.cookies[SESSION_COOKIE_NAME]["path"], "/example/")

    def test_age_session_cookie(self):
        with self.settings(AUTH_SESSION_COOKIE_AGE=10):
            response = self.middleware(self.request)
            self.assertEqual(response.cookies[SESSION_COOKIE_NAME]["max-age"], 10)
        with self.settings(AUTH_SESSION_COOKIE_AGE=60 * 60 * 24):
            response = self.middleware(self.request)
            self.assertEqual(response.cookies[SESSION_COOKIE_NAME]["max-age"], 86400)

    def test_name_session_cookie(self):
        with self.settings(AUTH_SESSION_COOKIE_NAME="custom"):
            response = self.middleware(self.request)
            self.assertIn("custom", response.cookies)
        with self.settings(AUTH_SESSION_COOKIE_NAME="session_key"):
            response = self.middleware(self.request)
            self.assertIn("session_key", response.cookies)
