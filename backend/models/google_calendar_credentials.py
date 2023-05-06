from datetime import datetime
from typing import TYPE_CHECKING, Optional, Set

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class GoogleCalendarCredentialsBase(SQLModel):
    token: str = Field(index=True, nullable=False)
    expiry: datetime = Field(index=True, nullable=False)
    refresh_token: str = Field(index=True, nullable=False)
    scopes: Set[str] = Field(index=True, nullable=False)
    user_id: str = Field(foreign_key="user.id", nullable=False)
    user: "User" = Relationship(back_populates="calendar_credentials")


class GoogleCalendarCredentials(GoogleCalendarCredentialsBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)


class GoogleCalendarCredentialsCreate(GoogleCalendarCredentialsBase):
    pass


class GoogleCalendarCredentialsRead(GoogleCalendarCredentialsBase):
    id: str
