from typing import Optional

from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models import StravaCredentials
from backend.schemas import StravaCredentialsCreate, StravaCredentialsUpdate
from backend.utils.base_utils import get_random_alphanumeric_string


class CRUDStravaCredentials(CRUDBase[StravaCredentials, StravaCredentialsCreate, StravaCredentialsUpdate]):
    def get_by_user_id(self, db: Session, user_id: str) -> Optional[StravaCredentials]:
        return db.query(StravaCredentials).filter(StravaCredentials.user_id == user_id).first()

    def create_and_add_to_user(self, db: Session, user_id: str, strava_credentials_obj: StravaCredentialsCreate):
        strava_credentials_db_obj: StravaCredentials = StravaCredentials(id = get_random_alphanumeric_string(12),
                                                                  access_token = strava_credentials_obj.access_token,
                                                                  expires_at = strava_credentials_obj.expires_at,
                                                                  refresh_token = strava_credentials_obj.refresh_token,
                                                                  user_id = user_id)
        db.add(strava_credentials_db_obj)
        db.commit()
        db.refresh(strava_credentials_db_obj)
        return strava_credentials_db_obj


strava_credentials = CRUDStravaCredentials(StravaCredentials)
