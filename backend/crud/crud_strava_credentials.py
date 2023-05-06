from typing import Optional

from sqlmodel import Session

from backend.models import StravaCredentials, StravaCredentialsCreate


def get_by_user_id(db: Session, user_id: str) -> Optional[StravaCredentials]:
    return db.query(StravaCredentials).filter(StravaCredentials.user_id == user_id).first()


def create_and_add_to_user(db: Session, strava_user_id: int, obj: StravaCredentialsCreate):
    db_obj: StravaCredentials = StravaCredentials.from_orm(obj)
    db_obj.id = strava_user_id
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
