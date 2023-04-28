import datetime
from typing import Optional, List

from pydantic import BaseModel


# Shared properties
class GoogleAuthBase(BaseModel):
    token: Optional[str]
    expiry: Optional[datetime.datetime]
    refresh_token: Optional[str]
    scopes: Optional[list]


class GoogleAuthCreate(BaseModel):
    token: str
    expiry: datetime.datetime
    refresh_token: str
    scopes: List[str]


class GoogleAuthUpdate(GoogleAuthBase):
    pass


class GoogleAuthInDBBase(GoogleAuthBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class GoogleAuth(GoogleAuthInDBBase):
    pass


# Additional properties stored in DB
class GoogleAuthInDB(GoogleAuthInDBBase):
    pass
