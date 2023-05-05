from typing import Optional

from sqlalchemy.orm import Session

from backend.models import GoogleCalendarAuth, User
from backend.utils.base_utils import get_random_alphanumeric_string


def get_for_user(db: Session, user_id: str) -> Optional[GoogleCalendarAuth]:
    return db.query(GoogleCalendarAuth).filter(User.id == user_id).first()


def create_and_add_to_user(db: Session, user_id: str, obj: GoogleCalendarAuthCreate):
    g
    google_auth_db_obj: GoogleCalendarAuth = GoogleCalendarAuth(id=get_random_alphanumeric_string(12),
                                                                token=google_auth_obj.token,
                                                                expiry=google_auth_obj.expiry,
                                                                refresh_token=google_auth_obj.refresh_token,
                                                                scopes=google_auth_obj.scopes)
    db.add(google_auth_db_obj)
    db.commit()
    db.refresh(google_auth_db_obj)
    return google_auth_db_obj
