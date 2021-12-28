from django.test import TestCase
from django.conf import settings


class DefaultTests(TestCase):
    def test_coming_soon_mode(self):
        error_message = "'Settings' object has no attribute 'COMING_SOON_MODE'"
        with self.assertRaisesMessage(AttributeError, error_message):
            self.assertEqual(settings.COMING_SOON_MODE, False)
            raise AttributeError(error_message)

    def test_maintenance_mode(self):
        error_message = "'Settings' object has no attribute 'MAINTENANCE_MODE'"
        with self.assertRaisesMessage(AttributeError, error_message):
            self.assertEqual(settings.MAINTENANCE_MODE, False)
            raise AttributeError(error_message)
