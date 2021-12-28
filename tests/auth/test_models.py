from jommerce.auth.models import CustomUser
from django.test import TestCase


class CustomUserModelTests(TestCase):
    model = CustomUser

    def test_convert_empty_email_values_to_none(self):
        self.assertIsNone(self.model.objects.create(username="user1").email)
        self.assertIsNone(self.model.objects.create(username="user2", email="").email)
        self.assertIsNone(self.model.objects.create(username="user3", email=None).email)
        self.assertIsNone(self.model.objects.get(username="user1").email)
        self.assertIsNone(self.model.objects.get(username="user2").email)
        self.assertIsNone(self.model.objects.get(username="user3").email)
