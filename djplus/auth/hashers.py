import secrets
import base64
import hashlib
from django.utils.crypto import pbkdf2, get_random_string, constant_time_compare


def generate_salt():
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    return "".join(secrets.choice(characters) for _ in range(32))


class PBKDF2PasswordHasher:
    def __init__(self, iterations=320000):
        self.iterations = iterations
        self._salt = None

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

    def _check_password(self, password):
        if not isinstance(password, str):
            raise TypeError("Password must be a string")

    def hash(self, password):
        self._check_password(password)
        hashed = pbkdf2(password, self.salt, self.iterations, digest=hashlib.sha256)
        hashed = base64.b64encode(hashed).decode("ascii").strip()
        hashed_password = "$".join((hashed, self.salt, str(self.iterations)))
        del self.salt
        return hashed_password

    def verify(self, raw_password, hashed_password):
        self._check_password(raw_password)
        hashed, self.salt, iterations = hashed_password.split("$")
        self.iterations = int(iterations)
        return constant_time_compare(hashed_password, self.hash(raw_password))
