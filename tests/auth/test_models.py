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


class SessionModelTests(TestCase):
    def setUp(self) -> None:
        self.session = Session()

    def test_default_session_id(self):
        max_length = Session._meta.get_field("id").max_length
        self.assertIsInstance(self.session.id, str)
        self.assertEqual(len(self.session.id), max_length)
        self.assertNotEqual(self.session.id, Session().id)

    def test_new_session(self):
        self.assertIs(self.session.modified, False)
        self.assertIs(self.session.accessed, False)

    def test_empty_session(self):
        self.assertIs(self.session.is_empty, True)
        self.session.user = User()
        self.assertIs(self.session.is_empty, False)
        self.session.user = None
        self.session["key"] = "value"
        self.assertIs(self.session.is_empty, False)
        self.session.data = {}
        self.assertIs(self.session.is_empty, True)

    def test_store_data_in_session(self):
        self.session["key"] = "value"
        self.assertEqual(self.session["key"], "value")

    def test_get(self):
        self.session["key"] = "value"
        self.session.modified = False
        self.session.accessed = False
        self.assertEqual(self.session.get("key"), "value")
        self.assertIs(self.session.accessed, True)

    def test_get_default(self):
        self.assertIsNone(self.session.get("key does not exist"))
        self.assertIs(self.session.accessed, True)

    def test_get_default_named_argument(self):
        self.assertEqual(self.session.get("key does not exist", default="test"), "test")
        self.assertIs(self.session.accessed, True)

    def test_values(self):
        self.assertEqual(list(self.session.values()), [])
        self.assertIs(self.session.accessed, True)
        self.session["key"] = "value"
        self.session.modified = False
        self.session.accessed = False
        self.assertEqual(list(self.session.values()), ["value"])
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, False)

    def test_keys(self):
        self.assertEqual(list(self.session.keys()), [])
        self.assertIs(self.session.accessed, True)
        self.session["key"] = "value"
        self.session.accessed = False
        self.session.modified = False
        self.assertEqual(list(self.session.keys()), ["key"])
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, False)
