import unittest
from unittest.mock import patch
from django.test import TestCase
from django.utils.crypto import get_random_string
from djplus.auth.hashers import (
    BasePasswordHasher,
    PBKDF2PasswordHasher,
    Argon2PasswordHasher,
    BcryptPasswordHasher,
    ScryptPasswordHasher,
)

try:
    import argon2
except ImportError:
    argon2 = None

try:
    import bcrypt
except ImportError:
    bcrypt = None


class BasePasswordHasherTest(TestCase):
    def test_abstract(self):
        expected_error = "Can't instantiate abstract class"
        with self.assertRaisesMessage(TypeError, expected_error):
            BasePasswordHasher()

    @patch("djplus.auth.hashers.BasePasswordHasher.__abstractmethods__", set())
    def test_salt_property(self):
        hasher = BasePasswordHasher()
        salt = hasher.salt
        self.assertEqual(salt, hasher.salt)

        del hasher.salt
        self.assertNotEqual(salt, hasher.salt)
        self.assertIsNotNone(hasher.salt)
        self.assertNotEqual(hasher.salt, "")

        hasher.salt = "my salt"
        self.assertEqual(hasher.salt, "my salt")

        del hasher.salt
        self.assertNotEqual(hasher.salt, "my salt")


class PasswordHasherTestMixin:
    password = get_random_string(length=6)

    @classmethod
    def setUpTestData(cls):
        cls.hashed_password = cls.hasher.hash(cls.password)

    def test_hash_password(self):
        self.assertNotEqual(self.password, self.hashed_password)

    def test_verify_hashed_password(self):
        self.assertTrue(self.hasher.verify(self.password, self.hashed_password))
        self.assertFalse(self.hasher.verify(get_random_string(length=6), self.hashed_password))

    def test_use_salt(self):
        hashed_password2 = self.hasher.hash(self.password)
        self.assertNotEqual(hashed_password2, self.hashed_password)

    def test_hashed_password_must_be_string(self):
        self.assertIsInstance(self.hashed_password, str)

    def test_hashed_password_must_not_be_blank(self):
        self.assertNotEqual(self.hashed_password, "")


class PBKDF2PasswordHasherTest(PasswordHasherTestMixin, TestCase):
    hasher = PBKDF2PasswordHasher(iterations=1)


@unittest.skipUnless(argon2, "argon2-cffi not installed")
class Argon2PasswordHasherTest(PasswordHasherTestMixin, TestCase):
    hasher = Argon2PasswordHasher()


@unittest.skipUnless(bcrypt, "bcrypt not installed")
class BcryptPasswordHasherTest(PasswordHasherTestMixin, TestCase):
    hasher = BcryptPasswordHasher()


class ScryptPasswordHasherTest(PasswordHasherTestMixin, TestCase):
    hasher = ScryptPasswordHasher()
