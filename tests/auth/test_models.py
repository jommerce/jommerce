from django.test import TestCase
from jommerce.auth.models import User


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(email="user1@gmail.com", password="123456")
        User.objects.create(email="user2@gmail.com", password="123456")
        User.objects.create(email="user3@gmail.com", password="123456")

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
