from datetime import datetime
from typing import Optional

from sqlmodel import Session

from backend.models import CalendarEvent, User, CalendarEventCreate
from backend.utils.base_utils import get_random_alphanumeric_string


def get_by_strava_event_id(db: Session, strava_event_id: int) -> Optional[CalendarEvent]:
    return db.query(CalendarEvent).filter(CalendarEvent.strava_event_id == strava_event_id).first()


def get_by_start_and_end_date(db: Session,
                              user_id: str,
                              start_date: datetime,
                              end_date: datetime) -> Optional[CalendarEvent]:
    return db.query(CalendarEvent).filter(User.id == user_id,
                                          CalendarEvent.start_date == start_date,
                                          CalendarEvent.end_date == end_date).first()


def create_and_add_to_user(db: Session, obj: CalendarEventCreate):
    new_obj: CalendarEvent = CalendarEvent(id=get_random_alphanumeric_string(20),
                                           start_date=obj.start_date,
                                           end_date=obj.end_date,
                                           strava_event_id=obj.strava_event_id,
                                           calendar_event_id=obj.calendar_event_id,
                                           user_id=obj.user_id)
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj

