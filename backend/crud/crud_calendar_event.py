from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models import CalendarEvent, User
from backend.schemas import CalendarEventCreate, CalendarEventUpdate
from backend.utils.base_utils import get_random_alphanumeric_string

class CRUDCalendarEvent(CRUDBase[CalendarEvent, CalendarEventCreate, CalendarEventUpdate]):
    def get_by_strava_event_id(self, db: Session, strava_event_id: int) -> Optional[CalendarEvent]:
        return db.query(CalendarEvent).filter(CalendarEvent.strava_event_id == strava_event_id).first()

    def get_by_start_and_end_date(self, db: Session, user_id: str, start_date: datetime, end_date: datetime) -> Optional[CalendarEvent]:
        return db.query(CalendarEvent).filter(User.id == user_id,
                                              CalendarEvent.start_date == start_date,
                                              CalendarEvent.end_date == end_date).first()

    def create_and_add_to_user(self, db: Session, user_id: str, obj_create: CalendarEventCreate):
        new_obj: CalendarEvent = CalendarEvent(id = get_random_alphanumeric_string(20),
                                               start_date = obj_create.start_date,
                                               end_date = obj_create.end_date,
                                               strava_event_id = obj_create.strava_event_id,
                                               calendar_event_id = obj_create.calendar_event_id,
                                               user_id = user_id)
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)
        return new_obj


calendar_event = CRUDCalendarEvent(CalendarEvent)
