from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CalendarEventBase(BaseModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    strava_event_id: Optional[int]
    calendar_event_id: Optional[str]


class CalendarEventCreate(BaseModel):
    start_date: datetime
    end_date: datetime
    strava_event_id: Optional[int]
    calendar_event_id: str


class CalendarEventUpdate(CalendarEventBase):
    pass


class CalendarEventInDBBase(CalendarEventBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


class CalendarEvent(CalendarEventInDBBase):
    pass


class CalendarEventInDB(CalendarEventInDBBase):
    pass
