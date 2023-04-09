from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models import StravaAuth
from backend.schemas import StravaAuthCreate, StravaAuthUpdate
from backend.utils.base_utils import get_random_alphanumeric_string


class CRUDStravaAuth(CRUDBase[StravaAuth, StravaAuthCreate, StravaAuthUpdate]):
    def create_and_add_to_user(self, db: Session, user_id: str, strava_auth_obj: StravaAuthCreate):
        strava_auth_db_obj: StravaAuth = StravaAuth(id = get_random_alphanumeric_string(12),
                                                    access_token = strava_auth_obj.access_token,
                                                    expires_at = strava_auth_obj.expires_at,
                                                    refresh_token = strava_auth_obj.refresh_token,
                                                    user_id = user_id)
        db.add(strava_auth_db_obj)
        db.commit()
        db.refresh(strava_auth_db_obj)
        return strava_auth_db_obj


strava_auth = CRUDStravaAuth(StravaAuth)
