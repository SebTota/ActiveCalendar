from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class StravaCredentialsBase(SQLModel):
    access_token: str = Field(nullable=False)
    expires_at: datetime = Field(nullable=False)
    refresh_token: str = Field(nullable=False)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    user: "User" = Relationship(back_populates="strava_credentials")


class StravaCredentials(StravaCredentialsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Also the athlete's Strava id


class StravaCredentialsCreate(StravaCredentialsBase):
    pass


class StravaCredentialsRead(StravaCredentialsBase):
    id: int  # Also the athlete's Strava id
