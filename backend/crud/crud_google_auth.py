from typing import Optional

from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models import GoogleAuth, User
from backend.schemas import GoogleAuthCreate, GoogleAuthUpdate
from backend.utils.base_utils import get_random_alphanumeric_string


class CRUDGoogleAuth(CRUDBase[GoogleAuth, GoogleAuthCreate, GoogleAuthUpdate]):

    def get_for_user(self, db: Session, user_id: str) -> Optional[GoogleAuth]:
        return db.query(GoogleAuth).filter(User.id == user_id).first()

    def create_and_add_to_user(self, db: Session, user_id: str, google_auth_obj: GoogleAuthCreate):
        google_auth_db_obj: GoogleAuth = GoogleAuth(id = get_random_alphanumeric_string(12),
                                                    token=google_auth_obj.token,
                                                    client_id = google_auth_obj.client_id,
                                                    client_secret = google_auth_obj.client_secret,
                                                    expiry = google_auth_obj.expiry,
                                                    refresh_token = google_auth_obj.refresh_token,
                                                    scopes = google_auth_obj.scopes,
                                                    user_id = user_id)
        db.add(google_auth_db_obj)
        db.commit()
        db.refresh(google_auth_db_obj)
        return google_auth_db_obj


google_auth = CRUDGoogleAuth(GoogleAuth)
