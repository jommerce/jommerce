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

    def test_get_full_name(self):
        user = self.model.objects.create(
            username="test1", first_name="Ali", last_name="Hashemi"
        )
        self.assertEqual(user.get_full_name(), "Ali Hashemi")
        user = self.model.objects.create(
            username="test2", first_name="Arash", last_name="Nowruzi"
        )
        self.assertEqual(user.get_full_name(), "Arash Nowruzi")
