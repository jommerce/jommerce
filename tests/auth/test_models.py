from django.test import TestCase
from jommerce.auth.models import User


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email="user1@gmail.com", password="123456")
        User.objects.create(email="user2@gmail.com", password="123456")
        User.objects.create(email="user3@gmail.com", password="password")

    def test_is_superuser(self):
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        user3 = User.objects.get(id=3)

        with self.settings(AUTH_SUPERUSER_ID=1):
            self.assertTrue(user1.is_superuser)
            self.assertFalse(user2.is_superuser)
            self.assertFalse(user3.is_superuser)

        with self.settings(AUTH_SUPERUSER_ID=2):
            self.assertFalse(user1.is_superuser)
            self.assertTrue(user2.is_superuser)
            self.assertFalse(user3.is_superuser)

        with self.settings(AUTH_SUPERUSER_ID=3):
            self.assertFalse(user1.is_superuser)
            self.assertFalse(user2.is_superuser)
            self.assertTrue(user3.is_superuser)

        with self.settings(AUTH_SUPERUSER_ID=None):
            self.assertFalse(user1.is_superuser)
            self.assertFalse(user2.is_superuser)
            self.assertFalse(user3.is_superuser)

    def test_is_authenticated(self):
        user = User.objects.get(id=1)
        self.assertTrue(user.is_authenticated)

    def test_is_anonymous(self):
        user = User.objects.get(id=1)
        self.assertFalse(user.is_anonymous)

    def test_password_hashing_with_salt(self):
        # Created
        user1 = User.objects.create(email="test1@gmail.com", password="123456")
        user2 = User.objects.create(email="test2@gmail.com", password="123456")
        self.assertNotEqual(user1.password, "123456")
        self.assertNotEqual(user2.password, "123456")
        self.assertNotEqual(user1.password, user2.password)

        # Updated
        user1.password = "password"
        user2.password = "password"
        user1.save()
        user2.save()
        self.assertNotEqual(user1.password, "password")
        self.assertNotEqual(user2.password, "password")
        self.assertNotEqual(user1.password, user2.password)

    def test_check_password(self):
        user1 = User.objects.create(email="test1@gmail.com", password="123456")
        self.assertTrue(user1.check_password("123456"))
        self.assertFalse(user1.check_password("password"))

        user2 = User.objects.create(email="test2@gmail.com", password="password")
        self.assertTrue(user2.check_password("password"))
        self.assertFalse(user2.check_password("123456"))
