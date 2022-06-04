import base64
import hashlib
import binascii
import functools
from abc import ABC, abstractmethod
from django.utils.encoding import force_bytes
from django.utils.crypto import constant_time_compare
from django.utils.module_loading import import_string
from django.conf import settings
from .utils import generate_random_string

try:
    import argon2
except ImportError:
    pass

try:
    import bcrypt
except ImportError:
    pass


def get_default_hasher():
    return import_string(settings.AUTH_PASSWORD_HASHER)


class BasePasswordHasher(ABC):
    @abstractmethod
    def hash(self, password):
        pass

    @abstractmethod
    def verify(self, raw_password, hashed_password):
        pass

    @staticmethod
    def generate_salt_if_none(func_=None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                self.salt = self.salt or generate_random_string(32, symbol=False)
                hashed_password = func(self, *args, **kwargs)
                self.salt = None
                return hashed_password
            return wrapper
        if func_ is None:
            return decorator
        else:
            return decorator(func_)


class PBKDF2PasswordHasher(BasePasswordHasher):
    def __init__(self, iterations=480_000, digest_name="sha256", salt=None, digest_size=None):
        self.iterations = iterations
        self.digest_name = digest_name
        self.salt = salt
        self.digest_size = digest_size or getattr(hashlib, digest_name)().digest_size

    @BasePasswordHasher.generate_salt_if_none
    def hash(self, password):
        hashed = hashlib.pbkdf2_hmac(
            self.digest_name,
            force_bytes(password),
            force_bytes(self.salt),
            self.iterations,
            dklen=self.digest_size,
        )
        hashed = base64.b64encode(hashed).decode("ascii").strip()
        return "$".join((self.digest_name, str(self.iterations), self.salt, hashed))

    def verify(self, raw_password, hashed_password):
        self.digest_name, iterations, self.salt, hashed = hashed_password.split("$")
        self.iterations = int(iterations)
        return constant_time_compare(hashed_password, self.hash(raw_password))


class Argon2PasswordHasher(BasePasswordHasher):
    def __init__(self, time_cost=2, memory_cost=102_400, parallelism=8, salt=None, hash_length=32, salt_length=16, type="argon2id", version=19):
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_length = hash_length
        self.salt_length = salt_length
        self.type = type
        self.version = version
        self.salt = salt

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

    @BasePasswordHasher.generate_salt_if_none
    def hash(self, password):
        return argon2.low_level.hash_secret(
            password.encode(),
            self.salt.encode(),
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=self.hash_length,
            type=self.type,
            version=self.version,
        ).decode("ascii")

    def verify(self, raw_password, hashed_password):
        try:
            return argon2.PasswordHasher().verify(hashed_password, raw_password)
        except argon2.exceptions.VerificationError:
            return False


class BcryptPasswordHasher(BasePasswordHasher):
    def __init__(self, digest=hashlib.sha256, rounds=12, salt=None):
        self.digest = digest
        self.rounds = rounds
        self.salt = salt

    def hash(self, password):
        password = password.encode()
        self.salt = self.salt or bcrypt.gensalt(self.rounds)
        if self.digest is not None:
            password = binascii.hexlify(self.digest(password).digest())
        hashed_password = bcrypt.hashpw(password, self.salt).decode("ascii")
        self.salt = None
        return hashed_password

    def verify(self, raw_password, hashed_password):
        self.salt = hashed_password.encode("ascii")
        return constant_time_compare(hashed_password, self.hash(raw_password))


class ScryptPasswordHasher(BasePasswordHasher):
    def __init__(self, block_size=8, parallelism=1, work_factor=2**14, maxmem=0, salt=None):
        self.block_size = block_size
        self.parallelism = parallelism
        self.work_factor = work_factor
        self.maxmem = maxmem
        self.salt = salt

    @BasePasswordHasher.generate_salt_if_none
    def hash(self, password):
        hash_ = hashlib.scrypt(
            password.encode(),
            salt=self.salt.encode(),
            n=self.work_factor,
            r=self.block_size,
            p=self.parallelism,
            maxmem=self.maxmem,
            dklen=64,
        )
        hash_ = base64.b64encode(hash_).decode("ascii").strip()
        return "$".join((str(self.work_factor), self.salt, str(self.block_size), str(self.parallelism), hash_))

    def verify(self, raw_password, hashed_password):
        work_factor, self.salt, block_size, parallelism, hashed = hashed_password.split("$")
        self.work_factor = int(work_factor)
        self.block_size = int(block_size)
        self.parallelism = int(parallelism)
        return constant_time_compare(hashed_password, self.hash(raw_password))
