import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class StravaCredentialsBase(BaseModel):
    access_token: str
    expires_at: datetime.datetime
    refresh_token: str


# Properties to receive via API on creation
class StravaCredentialsCreate(StravaCredentialsBase):
    pass


class StravaCredentialsUpdate(StravaCredentialsCreate):
    pass


class StravaCredentialsInDBBase(StravaCredentialsBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class StravaCredentials(StravaCredentialsInDBBase):
    pass


# Additional properties stored in DB
class StravaCredentialsInDB(StravaCredentialsInDBBase):
    pass
