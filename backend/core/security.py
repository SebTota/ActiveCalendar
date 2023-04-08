from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer

from backend.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_account_verification_token(email: str) -> str:
    """
    Generate an account verification token that is URL safe
    """
    url_serializer = URLSafeTimedSerializer(settings.EMAIL_ACCOUNT_VERIFICATION_SECRET_KEY)
    return url_serializer.dumps(email, settings.EMAIL_ACCOUNT_VERIFICATION_SALT)


def confirm_account_verification_token(token: str, email: str) -> bool:
    serializer = URLSafeTimedSerializer(settings.EMAIL_ACCOUNT_VERIFICATION_SECRET_KEY)
    try:
        deserialized_email = serializer.loads(token, salt=settings.EMAIL_ACCOUNT_VERIFICATION_SALT, max_age=3600)
        return email == deserialized_email
    except Exception:
        return False
