from django.test import TestCase
from django.utils.crypto import get_random_string
from djplus.auth.hashers import PBKDF2PasswordHasher


class PBKDF2PasswordHasherTests(TestCase):
    password = get_random_string(length=6)
    hasher = PBKDF2PasswordHasher()
    hashed_password = hasher.hash(password)

    def test_hash_password(self):
        self.assertNotEqual(self.password, self.hashed_password)

    def test_verify_hashed_password(self):
        self.assertTrue(self.hasher.verify(self.password, self.hashed_password))
        self.assertFalse(self.hasher.verify(get_random_string(length=6), self.hashed_password))

    def test_use_salt(self):
        hashed_password2 = self.hasher.hash(self.password)
        self.assertNotEqual(hashed_password2, self.hashed_password)

    def test_invalid_password(self):
        expected_error = "Password must be a string"
        for password in {1, 3.14, None, b"bytes_password"}:
            with self.assertRaisesMessage(TypeError, expected_error):
                self.hasher.hash(password)

    def test_hashed_password_must_be_string(self):
        self.assertIsInstance(self.hashed_password, str)

    def test_hashed_password_must_not_be_blank(self):
        self.assertNotEqual(self.hashed_password, "")
