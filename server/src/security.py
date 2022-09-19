from passlib.context import CryptContext
from cryptography.fernet import Fernet
import os
from typing import Union
from fastapi import HTTPException, status, Cookie
from .model import Users

class Security:

    fernet = Fernet(os.environ["CRYPT_KEY"])
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hash_password(password: str):
        return Security.pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str):
        return Security.pwd_context.verify(password, hashed_password)

    @staticmethod
    def encrypt_cookie(text: str) -> str:
        return Security.fernet.encrypt(text.encode()).decode()

    @staticmethod
    def decrypt_cookie(text: str) -> str:
        return Security.fernet.decrypt(text.encode()).decode()


async def require_user(user: Union[str, None] = Cookie(default=None)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    decrypted_user_key = Security.decrypt_cookie(user)
    return {"user_auth": Users.get(decrypted_user_key)}

