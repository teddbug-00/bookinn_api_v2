import hashlib
import secrets
from functools import lru_cache

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

from src.core.config import settings


@lru_cache
def get_password_hasher():
    return PasswordHasher(
        time_cost=1,
        memory_cost=8192,
        parallelism=2,
        hash_len=32,
        salt_len=16
    )

password_hasher = get_password_hasher()


def verify_password(raw_password: str, password_salt: str, hashed_password: str) -> bool:
    try:
        peppered_password = hashlib.sha256((raw_password + settings.PASSWORD_PEPPER + password_salt).encode()).hexdigest()

        return password_hasher.verify(hashed_password, peppered_password)

    except (VerifyMismatchError, InvalidHash):
        return False


class Passwords:
    def __init__(self):
        self.settings = settings

    @staticmethod
    def get_password_hash(raw_password: str) -> tuple:
        
        password_salt = secrets.token_hex(16)

        peppered_password = hashlib.sha256((raw_password + settings.PASSWORD_PEPPER + password_salt).encode()).hexdigest()

        hashed_password = password_hasher.hash(peppered_password)

        return hashed_password, password_salt


passwords = Passwords()