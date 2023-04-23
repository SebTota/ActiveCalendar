from typing import Optional

from requests import Session

from backend import schemas, crud
from backend.accessors import StravaAccessor
from backend.core import logger
from backend.db.session import SessionLocal
from backend.models import User, StravaCredentials


class StravaNotificationProcessor:

    def __init__(self):
        self._db: Session = SessionLocal()

    def process(self, notification: schemas.StravaNotification):
        strava_credentials: Optional[StravaCredentials] = crud.strava_credentials.get(self._db, notification.owner_id)
        if strava_credentials is None:
            logger.error(f"Failed to process Strava notification for user: {notification.owner_id} "
                         f"activity: {notification.object_id} because the user has not authed with Strava")
            return

        strava_accessor: StravaAccessor = StravaAccessor(strava_credentials)
        logger.info(f"Strava activity: {strava_accessor.get_activity(notification.object_id)}")


strava_notification_processor: StravaNotificationProcessor = StravaNotificationProcessor()
