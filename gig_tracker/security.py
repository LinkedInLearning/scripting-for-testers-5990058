from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError

from .schema.user import User

SECRET_KEY = "c06497d1ff90e59d21d5bd57ba5160243e537ca69d999bba19772c1363ba43c8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(
        bytes(plain_password, encoding="utf-8"),
        bytes(hashed_password, encoding="utf-8"),
    )


def hash_password(password) -> bytes:
    return bcrypt.hashpw(bytes(password, encoding="utf-8"), bcrypt.gensalt())


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return False
    except InvalidTokenError:
        return False

    return True


def authenticate_user(user: User | None, password: str) -> User | bool:
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True
