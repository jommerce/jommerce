from django.test import TestCase, override_settings
from django.utils import timezone
from djplus.auth.models import User, AnonymousUser, Session
from djplus.auth.utils import generate_random_string


@override_settings(AUTH_PASSWORD_HASHERS=["tests.auth.test_hashers.pbkdf2_hasher"])
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email="user1@gmail.com", password="123456")
        User.objects.create(email="user2@gmail.com", password="123456")
        User.objects.create(email="user3@gmail.com", password="password")

    def test_password_hashing_with_salt(self):
        user1 = User.objects.get(pk=1)
        self.assertNotEqual(user1.password, "123456")
        user2 = User.objects.get(pk=2)
        self.assertNotEqual(user2.password, "123456")
        self.assertNotEqual(user1.password, user2.password)

    def test_verify_password(self):
        user = User.objects.get(pk=1)
        self.assertTrue(user.verify_password("123456"))
        self.assertFalse(user.verify_password("password"))

        user = User.objects.get(pk=3)
        self.assertTrue(user.verify_password("password"))
        self.assertFalse(user.verify_password("123456"))

    def test_is_authenticated(self):
        user = User.objects.get(pk=1)
        self.assertTrue(user.is_authenticated)

        with self.assertRaisesMessage(AttributeError, "can't set attribute 'is_authenticated'"):
            user.is_authenticated = False

    def test_is_anonymous(self):
        user = User.objects.get(pk=1)
        self.assertFalse(user.is_anonymous)

        with self.assertRaisesMessage(AttributeError, "can't set attribute 'is_anonymous'"):
            user.is_anonymous = True

    def test_upgrade_password_hasher(self):
        password = generate_random_string(length=12)
        with self.settings(AUTH_PASSWORD_HASHERS=[
            "tests.auth.test_hashers.pbkdf2_hasher",
            "tests.auth.test_hashers.scrypt_hasher",
        ]):
            user = User.objects.create(email="test@gmail.com", password=password)
            self.assertTrue(user.verify_password(password))

        with self.settings(AUTH_PASSWORD_HASHERS=["tests.auth.test_hashers.scrypt_hasher"]):
            self.assertFalse(user.verify_password(password))

        with self.settings(AUTH_PASSWORD_HASHERS=["tests.auth.test_hashers.pbkdf2_hasher"]):
            self.assertTrue(user.verify_password(password))

        with self.settings(AUTH_PASSWORD_HASHERS=[
            "tests.auth.test_hashers.scrypt_hasher",
            "tests.auth.test_hashers.pbkdf2_hasher",
        ]):
            self.assertTrue(user.verify_password(password))

        with self.settings(AUTH_PASSWORD_HASHERS=["tests.auth.test_hashers.scrypt_hasher"]):
            self.assertTrue(user.verify_password(password))

        with self.settings(AUTH_PASSWORD_HASHERS=["tests.auth.test_hashers.pbkdf2_hasher"]):
            self.assertFalse(user.verify_password(password))


class AnonymousUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AnonymousUser()

    def test_is_authenticated(self):
        self.assertFalse(self.user.is_authenticated)
        with self.assertRaisesMessage(AttributeError, "can't set attribute 'is_authenticated'"):
            self.user.is_authenticated = True

    def test_is_anonymous(self):
        self.assertTrue(self.user.is_anonymous)
        with self.assertRaisesMessage(AttributeError, "can't set attribute 'is_anonymous'"):
            self.user.is_anonymous = False


class SessionModel(TestCase):
    def test_generate_session_id(self):
        length = Session._meta.get_field("id").max_length
        self.assertEqual(len(Session().id), length)
        self.assertIsInstance(Session().id, str)
        session = Session.objects.create()
        self.assertEqual(len(session.id), length)
        self.assertIsInstance(session.id, str)

    def test_a_empty_session(self):
        session = Session()
        self.assertTrue(session.is_empty)

    def test_a_full_session(self):
        session = Session(user=User())
        self.assertFalse(session.is_empty)
        session = Session(data={"key": "value"})
        self.assertFalse(session.is_empty)

    def test_store_data_in_session(self):
        session = Session()
        try:
            session["key"] = "value"
        except TypeError as err:
            self.fail(err)
        try:
            self.assertEqual(session["key"], "value")
        except TypeError as err:
            self.fail(err)
