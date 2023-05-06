from typing import TYPE_CHECKING, Optional

from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, BigInteger

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class CalendarEventBase(SQLModel):
    start_date: datetime = Field(index=True, nullable=False)
    end_date: datetime = Field(index=True, nullable=False)
    strava_event_id: Optional[int] = Field(index=True, default=None, sa_column=Column(BigInteger(), primary_key=True, autoincrement=False))
    calendar_event_id: str = Field(index=True, nullable=False)
    user_id: str = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="calendar_events")


class CalendarEvent(CalendarEventBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)


class CalendarEventCreate(CalendarEventBase):
    pass


class CalendarEventRead(CalendarEventBase):
    id: str
