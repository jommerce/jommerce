import base64
import hashlib
import secrets
import binascii
import functools
from abc import ABC, abstractmethod
from django.conf import settings
from django.utils.module_loading import import_string
from .utils import generate_random_string

try:
    import argon2
except ImportError:
    pass

try:
    import bcrypt
except ImportError:
    pass


@functools.lru_cache
def get_hashers():
    return [import_string(hasher_path) for hasher_path in settings.AUTH_PASSWORD_HASHERS]


class BasePasswordHasher(ABC):
    salt_length = 32

    @abstractmethod
    def hash(self, password, salt=None):
        pass

    def verify(self, raw_password, hashed_password):
        salt = hashed_password[:self.salt_length]
        return secrets.compare_digest(hashed_password.encode(), self.hash(raw_password, salt).encode())


class PBKDF2PasswordHasher(BasePasswordHasher):
    def __init__(self, iterations=480_000, digest_name="sha256", digest_size=None, salt_length=32):
        self.iterations = iterations
        self.digest_name = digest_name
        self.digest_size = digest_size
        self.salt_length = salt_length

    def hash(self, password, salt=None):
        salt = salt or generate_random_string(self.salt_length, symbol=False)
        hashed = hashlib.pbkdf2_hmac(
            self.digest_name,
            password.encode(),
            salt.encode(),
            self.iterations,
            dklen=self.digest_size,
        )
        hashed = base64.b64encode(hashed).decode("ascii").strip()
        return salt + hashed


class Argon2PasswordHasher(BasePasswordHasher):
    def __init__(self, time_cost=2, memory_cost=102_400, parallelism=8, hash_length=32, salt_length=16, type="argon2id", version=19):
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_length = hash_length
        self.salt_length = salt_length
        self.version = version

        if type == "argon2id":
            self.type = argon2.Type.ID
        elif type == "argon2d":
            self.type = argon2.Type.D
        elif type == "argon2i":
            self.type = argon2.Type.I
        else:
            raise ValueError("'type' must be one of these values. {'argon2id', 'argon2i', 'argon2d'}")

    def hash(self, password, salt=None):
        salt = salt or generate_random_string(self.salt_length, symbol=False)
        hashed = argon2.low_level.hash_secret(
            password.encode(),
            salt.encode(),
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=self.hash_length,
            type=self.type,
            version=self.version,
        ).decode("ascii").rsplit("$", 1)[1]
        return salt + hashed


class BcryptPasswordHasher(BasePasswordHasher):
    def __init__(self, digest=hashlib.sha256, rounds=12, prefix=b"2b"):
        self.digest = digest
        self.rounds = "0" + str(rounds) if rounds < 10 else str(rounds)
        self.prefix = prefix

    def hash(self, password, salt=None):
        password = password.encode()
        if self.digest is not None:
            password = binascii.hexlify(self.digest(password).digest())
        return bcrypt.hashpw(password, bcrypt.gensalt(int(self.rounds), self.prefix)).decode("ascii").rsplit("$", 1)[1]

    def verify(self, raw_password, hashed_password):
        password = raw_password.encode()
        if self.digest is not None:
            password = binascii.hexlify(self.digest(password).digest())
        return bcrypt.checkpw(
            password,
            b"$" + self.prefix + b"$" + str(self.rounds).encode() + b"$" + hashed_password.encode(),
        )


class ScryptPasswordHasher(BasePasswordHasher):
    def __init__(self, block_size=8, parallelism=1, work_factor=2**14, maxmem=0, salt_length=32):
        self.block_size = block_size
        self.parallelism = parallelism
        self.work_factor = work_factor
        self.maxmem = maxmem
        self.salt_length = salt_length

    def hash(self, password, salt=None):
        salt = salt or generate_random_string(self.salt_length, symbol=False)
        hash_ = hashlib.scrypt(
            password.encode(),
            salt=salt.encode(),
            n=self.work_factor,
            r=self.block_size,
            p=self.parallelism,
            maxmem=self.maxmem,
            dklen=64,
        )
        hash_ = base64.b64encode(hash_).decode("ascii").strip()
        return salt + hash_


default = PBKDF2PasswordHasher(iterations=480_000, digest_name="sha256", digest_size=None, salt_length=32)
