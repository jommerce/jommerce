from django.test import TestCase, override_settings
from django.utils import timezone
from djplus.auth.models import User, AnonymousUser, Session


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email="test@example.com", password="123456")

    def test_use_salt_in_password_hashing(self):
        user = User.objects.create(email="user@gmail.com", password="123456")
        self.assertNotEqual(self.user.password, "123456")
        self.assertNotEqual(user.password, "123456")
        self.assertNotEqual(self.user.password, user.password)

    def test_verify_password(self):
        self.assertIs(self.user.verify_password("123456"), True)
        self.assertIs(self.user.verify_password("password"), False)
        user = User.objects.create(email="user@gmail.com", password="password")
        self.assertIs(user.verify_password("123456"), False)
        self.assertIs(user.verify_password("password"), True)

    def test_is_authenticated(self):
        self.assertIs(self.user.is_authenticated, True)
        with self.assertRaises(AttributeError):
            self.user.is_authenticated = False

    def test_is_anonymous(self):
        self.assertIs(self.user.is_anonymous, False)
        with self.assertRaises(AttributeError):
            self.user.is_anonymous = True

    def test_upgrade_password_hasher(self):
        password = "p@ssword"
        with self.settings(AUTH_PASSWORD_HASHERS=[
            "tests.auth.test_hashers.pbkdf2_hasher",
            "tests.auth.test_hashers.scrypt_hasher",
        ]):
            user = User.objects.create(email="user@gmail.com", password=password)
            self.assertIs(user.verify_password(password), True)
        with self.settings(AUTH_PASSWORD_HASHERS=["tests.auth.test_hashers.scrypt_hasher"]):
            self.assertIs(user.verify_password(password), False)
        with self.settings(AUTH_PASSWORD_HASHERS=["tests.auth.test_hashers.pbkdf2_hasher"]):
            self.assertIs(user.verify_password(password), True)
        with self.settings(AUTH_PASSWORD_HASHERS=[
            "tests.auth.test_hashers.scrypt_hasher",
            "tests.auth.test_hashers.pbkdf2_hasher",
        ]):
            self.assertIs(user.verify_password(password), True)
        with self.settings(AUTH_PASSWORD_HASHERS=["tests.auth.test_hashers.scrypt_hasher"]):
            self.assertIs(user.verify_password(password), True)
        with self.settings(AUTH_PASSWORD_HASHERS=["tests.auth.test_hashers.pbkdf2_hasher"]):
            self.assertIs(user.verify_password(password), False)


class AnonymousUserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = AnonymousUser()

    def test_is_authenticated(self):
        self.assertIs(self.user.is_authenticated, False)
        with self.assertRaises(AttributeError):
            self.user.is_authenticated = True  # noqa

    def test_is_anonymous(self):
        self.assertIs(self.user.is_anonymous, True)
        with self.assertRaises(AttributeError):
            self.user.is_anonymous = False  # noqa


class SessionModelTests(TestCase):
    def setUp(self) -> None:
        self.session = Session(data={"key": "value"})

    def test_default_session_id(self):
        max_length = Session._meta.get_field("id").max_length
        self.assertIsInstance(self.session.id, str)
        self.assertEqual(len(self.session.id), max_length)
        self.assertNotEqual(self.session.id, Session().id)

    @override_settings(AUTH_SESSION_COOKIE_AGE=10)
    def test_default_expire_date(self):
        self.assertEqual(Session().expire_date, timezone.now() + timezone.timedelta(seconds=10))

    def test_new_session(self):
        self.assertIs(self.session.modified, False)
        self.assertIs(self.session.accessed, False)

    def test_has_key(self):
        self.assertIn("key", self.session)
        self.assertIs(self.session.accessed, True)

    def test_store_data_in_session(self):
        self.session["test key"] = "test value"
        self.assertEqual(self.session["test key"], "test value")
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, True)

    def test_delete_data_in_session(self):
        del self.session["key"]
        self.assertNotIn("key", self.session.data)
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, True)

    def test_do_not_save_empty_sessions(self):
        self.session.user = None
        self.session.data = {}
        self.session.save()
        with self.assertRaises(Session.DoesNotExist):  # noqa
            Session.objects.get(pk=self.session.id)

    def test_get(self):
        self.assertEqual(self.session.get("key"), "value")
        self.assertIs(self.session.accessed, True)

    def test_get_default(self):
        self.assertIsNone(self.session.get("key does not exist"))
        self.assertIs(self.session.accessed, True)

    def test_get_default_named_argument(self):
        self.assertEqual(self.session.get("key does not exist", default="test"), "test")
        self.assertIs(self.session.accessed, True)

    def test_values(self):
        self.assertEqual(list(self.session.values()), ["value"])
        self.assertIs(self.session.accessed, True)

    def test_keys(self):
        self.assertEqual(list(self.session.keys()), ["key"])
        self.assertIs(self.session.accessed, True)

    def test_items(self):
        self.assertEqual(list(self.session.items()), [("key", "value")])
        self.assertIs(self.session.accessed, True)

    def test_clear(self):
        self.session.clear()
        self.assertEqual(self.session.data, {})
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, True)

    def test_setdefault(self):
        self.assertEqual(self.session.setdefault("key"), "value")
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, False)

    def test_setdefault_default(self):
        self.assertIsNone(self.session.setdefault("test key"))
        self.assertIn("test key", self.session.data)
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, True)

    def test_setdefault_default_named_argument(self):
        self.assertEqual(self.session.setdefault("test key", default="test value"), "test value")
        self.assertIn("test key", self.session.data)
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, True)

    def test_update(self):
        self.session.update({"test key": "test value", "key": "changed value"})
        self.assertIn("key", self.session.data)
        self.assertIn("test key", self.session.data)
        self.assertEqual(self.session["key"], "changed value")
        self.assertEqual(self.session["test key"], "test value")
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, True)

