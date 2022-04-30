from django.test import TestCase
from djplus.auth.hashers import generate_salt


class TestUtilsHashPass(TestCase):
    def test_generate_salt(self):
        salt1 = generate_salt()
        self.assertEqual(len(salt1), 32)
        salt2 = generate_salt()
        self.assertEqual(len(salt2), 32)
        salt3 = generate_salt()
        self.assertEqual(len(salt3), 32)

        self.assertNotEqual(salt1, salt2)
        self.assertNotEqual(salt2, salt3)
        self.assertNotEqual(salt1, salt3)
