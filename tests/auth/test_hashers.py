import unittest
from django.test import TestCase
from dj.auth.utils import generate_random_string
from dj.auth.hashers import (
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

pbkdf2_hasher = PBKDF2PasswordHasher(iterations=1)
scrypt_hasher = ScryptPasswordHasher(work_factor=2)
argon2_hasher = Argon2PasswordHasher(memory_cost=8, time_cost=1, parallelism=1)
bcrypt_hasher = BcryptPasswordHasher(rounds=4)


class BasePasswordHasherTest(TestCase):
    def test_abstract(self):
        expected_error = "Can't instantiate abstract class"
        with self.assertRaisesMessage(TypeError, expected_error):
            BasePasswordHasher()


class PasswordHasherTestMixin:
    password = generate_random_string(length=6)

    @classmethod
    def setUpTestData(cls):
        cls.hashed_password = cls.hasher.hash(cls.password)

    def test_hash_password(self):
        self.assertNotEqual(self.password, self.hashed_password)

    def test_verify_hashed_password(self):
        self.assertTrue(self.hasher.verify(self.password, self.hashed_password))
        self.assertFalse(
            self.hasher.verify(generate_random_string(length=6), self.hashed_password)
        )

    def test_use_salt(self):
        hashed_password2 = self.hasher.hash(self.password)
        self.assertNotEqual(hashed_password2, self.hashed_password)

    def test_hashed_password_must_be_string(self):
        self.assertIsInstance(self.hashed_password, str)

    def test_hashed_password_must_not_be_blank(self):
        self.assertNotEqual(self.hashed_password, "")


class PBKDF2PasswordHasherTest(PasswordHasherTestMixin, TestCase):
    hasher = pbkdf2_hasher


@unittest.skipUnless(argon2, "argon2-cffi not installed")
class Argon2PasswordHasherTest(PasswordHasherTestMixin, TestCase):
    hasher = argon2_hasher


@unittest.skipUnless(bcrypt, "bcrypt not installed")
class BcryptPasswordHasherTest(PasswordHasherTestMixin, TestCase):
    hasher = bcrypt_hasher


class ScryptPasswordHasherTest(PasswordHasherTestMixin, TestCase):
    hasher = scrypt_hasher
