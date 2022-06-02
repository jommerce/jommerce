import base64
import hashlib
from abc import ABC, abstractmethod
from django.utils.encoding import force_bytes
from django.utils.crypto import constant_time_compare
from .utils import generate_random_string

try:
    import argon2
except ImportError:
    pass


class BasePasswordHasher(ABC):
    _salt = None

    @property
    def salt(self):
        self._salt = self._salt or generate_random_string(length=32, symbol=False)
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
    def __init__(self, iterations=480_000, digest_name="sha256", digest_size=None):
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
    def __init__(self, time_cost=2, memory_cost=102_400, parallelism=8, hash_length=32, salt_length=16, type="argon2id", version=19):
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_length = hash_length
        self.salt_length = salt_length
        self.type = type
        self.version = version

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value == "argon2id":
            self._type = argon2.Type.ID
        elif value == "argon2i":
            self._type = argon2.Type.I
        elif value == "argon2d":
            self._type = argon2.Type.D
        else:
            raise ValueError("'type' must be one of these values. {'argon2id', 'argon2i', 'argon2d'}")

    def hash(self, password):
        hashed_password = argon2.low_level.hash_secret(
            password.encode(),
            self.salt.encode(),
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=self.hash_length,
            type=self.type,
            version=self.version,
        ).decode("ascii")
        del self.salt
        return hashed_password

    def verify(self, raw_password, hashed_password):
        try:
            return argon2.PasswordHasher().verify(hashed_password, raw_password)
        except argon2.exceptions.VerificationError:
            return False


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
