from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer

from backend.core.config import settings
from backend.models import User, Token, TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_auth_token(user: User) -> Token:
    access_token_expires: datetime = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode: TokenPayload = TokenPayload(exp=access_token_expires, sub=str(user.id))
    encoded_jwt = jwt.encode(to_encode.dict(), settings.SECRET_KEY, algorithm=ALGORITHM)

    return Token(token_type='bearer',
                 access_token=encoded_jwt,
                 access_token_expires=access_token_expires)


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


def confirm_account_verification_token(token: str) -> Optional[str]:
    serializer = URLSafeTimedSerializer(settings.EMAIL_ACCOUNT_VERIFICATION_SECRET_KEY)
    try:
        return serializer.loads(token, salt=settings.EMAIL_ACCOUNT_VERIFICATION_SALT, max_age=3600)
    except Exception:
        return None
