from django.test import TestCase
from djplus.auth.models import User


class UserModelTest(TestCase):
    def test_password_hashing_with_salt(self):
        user1 = User.objects.create(email="user1@gmail.com", password="123456")
        self.assertNotEqual(user1.password, "123456")
        user2 = User.objects.create(email="user2@gmail.com", password="123456")
        self.assertNotEqual(user2.password, "123456")
        self.assertNotEqual(user1.password, user2.password)
