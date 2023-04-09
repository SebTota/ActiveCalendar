import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class StravaAuthBase(BaseModel):
    access_token: str
    expires_at: datetime.datetime
    refresh_token: str


# Properties to receive via API on creation
class StravaAuthCreate(StravaAuthBase):
    pass


class StravaAuthUpdate(StravaAuthCreate):
    pass


class StravaAuthInDBBase(StravaAuthBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class StravaAuth(StravaAuthInDBBase):
    pass


# Additional properties stored in DB
class StravaAuthInDB(StravaAuthInDBBase):
    pass
