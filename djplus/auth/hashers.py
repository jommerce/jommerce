import base64
import hashlib
from abc import ABC, abstractmethod
from django.utils.encoding import force_bytes
from django.utils.crypto import get_random_string, constant_time_compare


class BasePasswordHasher(ABC):
    _salt = None

    @property
    def salt(self):
        self._salt = self._salt or get_random_string(length=32)
        return self._salt

    @salt.setter
    def salt(self, value):
        self._salt = str(value)

    @salt.deleter
    def salt(self):
        self._salt = None

    @abstractmethod
    def hash(self, password):
        pass

    @abstractmethod
    def verify(self, raw_password, hashed_password):
        pass


class PBKDF2PasswordHasher(BasePasswordHasher):
    def __init__(self, iterations=320000, digest_name="sha256", digest_size=None):
        self.iterations = iterations
        self.digest_name = digest_name
        self.digest_size = digest_size or getattr(hashlib, digest_name)().digest_size

    def hash(self, password):
        hashed = hashlib.pbkdf2_hmac(
            self.digest_name,
            force_bytes(password),
            force_bytes(self.salt),
            self.iterations,
            dklen=self.digest_size,
        )
        hashed = base64.b64encode(hashed).decode("ascii").strip()
        hashed_password = "$".join((self.digest_name, str(self.digest_size), str(self.iterations), self.salt, hashed))
        del self.salt
        return hashed_password

    def verify(self, raw_password, hashed_password):
        self.digest_name, digest_size, iterations, self.salt, hashed = hashed_password.split("$")
        self.iterations = int(iterations)
        self.digest_size = int(digest_size)
        return constant_time_compare(hashed_password, self.hash(raw_password))


class Argon2PasswordHasher(BasePasswordHasher):
    def hash(self, password):
        pass

    def verify(self, raw_password, hashed_password):
        pass


class BcryptPasswordHasher(BasePasswordHasher):
    def hash(self, password):
        pass

    def verify(self, raw_password, hashed_password):
        pass


class ScryptPasswordHasher(BasePasswordHasher):
    def hash(self, password):
        pass

    def verify(self, raw_password, hashed_password):
        pass
