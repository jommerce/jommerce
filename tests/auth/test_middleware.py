from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from djplus.auth.middleware import AuthenticationMiddleware, AnonymousUser
from djplus.auth.models import User, Session

SESSION_COOKIE_NAME = settings.AUTH_SESSION_COOKIE_NAME


class IdentifyUser(TestCase):
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
        Session.objects.create(id="anonymous_session", ip="127.0.0.1",
                               expire_date=timezone.now() + timezone.timedelta(1))

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
        user = User.objects.create(username="test", email="test@example.com", password="123456")
        session = Session.objects.create(id="user_session", user=user, ip="127.0.0.1",
                                         expire_date=timezone.now() + timezone.timedelta(1))

        self.request.COOKIES[SESSION_COOKIE_NAME] = "user_session"
        self.middleware(self.request)
        self.assertIsInstance(self.request.user, User)
        self.assertIsNotNone(self.request.session.user)
        self.assertEqual(self.request.user, user)
        self.assertEqual(self.request.session, session)
        self.assertEqual(self.request.session.user, user)
