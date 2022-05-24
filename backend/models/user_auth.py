import os
import jwt
from typing import Optional
from fastapi import HTTPException, Cookie

ALGORITHM = 'HS256'
SECRET_KEY = os.getenv('COOKIE_SECRET_KEY')


class UserAuth:
    def __init__(self, user_id: str, expires: int):
        self.user_id = user_id
        self.expires = expires

    @staticmethod
    def from_dict(source):
        return UserAuth(**source)

    def to_dict(self):
        return self.__dict__


def update_session_cookie(data: UserAuth) -> str:
    return jwt.encode(data.to_dict(), SECRET_KEY, algorithm=ALGORITHM)


def decrypt_session_cookie(cookie: str) -> UserAuth:
    return UserAuth.from_dict(jwt.decode(cookie, SECRET_KEY, algorithms=[ALGORITHM]))


async def get_signed_in_user_auth(Authentication: Optional[str] = Cookie(None)) -> UserAuth:
    if Authentication is None:
        raise HTTPException(status_code=401, detail='User not signed in')

    auth_cookie: UserAuth = decrypt_session_cookie(Authentication)
    return auth_cookie
