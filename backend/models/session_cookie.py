import os
import jwt

ALGORITHM = 'HS256'
SECRET_KEY = os.getenv('COOKIE_SECRET_KEY')


class SessionCookie:
    def __init__(self, user_id: str, expires: int):
        self.user_id = user_id
        self.expires = expires

    @staticmethod
    def from_dict(source):
        return SessionCookie(**source)

    def to_dict(self):
        return self.__dict__


def update_session_cookie(data: SessionCookie) -> str:
    return jwt.encode(data.to_dict(), SECRET_KEY, algorithm=ALGORITHM)


def decrypt_session_cookie(cookie: str) -> SessionCookie:
    return SessionCookie.from_dict(jwt.decode(cookie, SECRET_KEY, algorithms=[ALGORITHM]))
