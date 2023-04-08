import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    token_type: str
    access_token: str
    access_token_expires: datetime.datetime
    refresh_token: str
    refresh_token_expires: datetime.datetime


class TokenPayload(BaseModel):
    sub: Optional[str] = None


# Request data when trying to refresh auth token using refresh token
class TokenRefreshRequest(BaseModel):
    refresh_token: str


class RefreshTokenBase(BaseModel):
    user_id: str
    refresh_token: str
    expires: datetime.datetime


class RefreshTokenCreate(RefreshTokenBase):
    id: str
    pass


# Empty model since we don't want to allow updates
class RefreshTokenUpdate(BaseModel):
    pass


# Refresh token stored in DB and mapped to specific user id
class RefreshTokenInDB(RefreshTokenBase):
    id: str
    pass


class RefreshToken(RefreshTokenBase):
    pass