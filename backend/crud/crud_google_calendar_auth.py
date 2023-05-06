from typing import Optional

from sqlmodel import Session

from backend.models import GoogleCalendarCredentials, User, GoogleCalendarCredentialsCreate
from backend.utils.base_utils import get_random_alphanumeric_string


def get_for_user(db: Session, user_id: str) -> Optional[GoogleCalendarCredentials]:
    return db.query(GoogleCalendarCredentials).filter(User.id == user_id).first()


def create(db: Session, obj: GoogleCalendarCredentialsCreate) -> GoogleCalendarCredentials:
    google_cal_auth_obj: GoogleCalendarCredentials = GoogleCalendarCredentials.from_orm(obj)
    google_cal_auth_obj.id = get_random_alphanumeric_string(12)
    db.add(google_cal_auth_obj)
    db.commit()
    db.refresh(google_cal_auth_obj)
    return google_cal_auth_obj


def remove(db: Session, obj: GoogleCalendarCredentials) -> GoogleCalendarCredentials:
    db.delete(obj)
    db.commit()
    return obj


def update(db: Session, obj: GoogleCalendarCredentials) -> GoogleCalendarCredentials:
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
