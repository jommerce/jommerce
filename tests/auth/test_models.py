from django.test import TestCase
from djplus.auth.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="user1", email="user1@gmail.com", password="123456")
        User.objects.create(username="user2", email="user2@gmail.com", password="123456")
        User.objects.create(username="user3", email="user3@gmail.com", password="password")

    def test_password_hashing_with_salt(self):
        user1 = User.objects.get(pk=1)
        self.assertNotEqual(user1.password, "123456")
        user2 = User.objects.get(pk=2)
        self.assertNotEqual(user2.password, "123456")
        self.assertNotEqual(user1.password, user2.password)

    def test_check_password(self):
        user = User.objects.get(pk=1)
        self.assertTrue(user.check_password("123456"))
        self.assertFalse(user.check_password("password"))

        user = User.objects.get(pk=3)
        self.assertTrue(user.check_password("password"))
        self.assertFalse(user.check_password("123456"))

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
