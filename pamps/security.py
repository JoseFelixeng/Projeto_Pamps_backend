"""Security utilities"""
from passlib.context import CryptContext
from pamps.config import settings
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.security.secret_key
ALGORITHM = settings.security.algorithm


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


class HashedPassword(str):
    """
    Takes a plain text password and hashes it.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type,
        handler: GetCoreSchemaHandler,
    ):
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):  # 👈 TEM QUE SER SÓ (cls, v)
        if not isinstance(v, str):
            raise TypeError("string required")

        # evita hash duplo
        if v.startswith("$2a$") or v.startswith("$2b$"):
            return cls(v)

        return cls(get_password_hash(v))
