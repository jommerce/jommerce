from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from djplus.auth.middleware import AuthenticationMiddleware, AnonymousUser
from djplus.auth.utils import generate_random_string
from djplus.auth.models import User, Session


class AuthenticationMiddlewareTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="test", email="test@example.com", password="123456")
        session = Session.objects.create(
            user=user,
            id=generate_random_string(length=32),
            expire_date=timezone.now() + timezone.timedelta(1),
            ip="127.0.0.1",
        )
        cls.user = user
        cls.session = session

    def setUp(self) -> None:
        self.request = RequestFactory().get("/")
        self.middleware = AuthenticationMiddleware(lambda req: HttpResponse())

    def test_the_session_key_is_not_in_the_cookie(self):
        self.middleware(self.request)
        self.assertIsInstance(self.request.user, AnonymousUser)
        self.assertIsNone(self.request.session)

    def test_the_session_key_does_not_exist_in_the_database(self):
        self.request.COOKIES[settings.AUTH_SESSION_COOKIE_NAME] = generate_random_string(length=32)
        self.middleware(self.request)
        self.assertIsInstance(self.request.user, AnonymousUser)
        self.assertIsNone(self.request.session)

    def test_the_session_key_does_exist_in_the_database(self):
        self.request.COOKIES[settings.AUTH_SESSION_COOKIE_NAME] = self.session.id
        self.middleware(self.request)
        self.assertNotIsInstance(self.request.user, AnonymousUser)
        self.assertIsNotNone(self.request.session)
