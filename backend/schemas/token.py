import datetime

from pydantic import BaseModel


class Token(BaseModel):
    token_type: str
    access_token: str
    access_token_expires: datetime.datetime


class TokenPayload(BaseModel):
    sub: str
    exp: datetime.datetime
