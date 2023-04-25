from typing import Optional

from stravalib.model import Activity

from backend import schemas, crud, models
from backend.accessors import StravaAccessor, GoogleCalendarAccessor
from backend.core import logger
from backend.db.session import SessionLocal
from backend.models import StravaCredentials
from backend.utils import calendar_template_utils


class StravaNotificationBackgroundTaskWorker:

    def __init__(self, notification: schemas.StravaNotification):
        self.notification: schemas.StravaNotification = notification
        self._db: SessionLocal = SessionLocal()
        self._init_accessors()

    def _init_accessors(self):
        strava_credentials: Optional[StravaCredentials] = crud.strava_credentials.get(self._db,
                                                                                      self.notification.owner_id)
        if strava_credentials is None:
            error: str = f"Failed to process Strava notification for user: {self.notification.owner_id} " \
                         f"activity: {self.notification.object_id} due to missing Strava Auth credentials."
            raise Exception(error)

        self.strava_credentials = strava_credentials
        self._user_id: str = strava_credentials.user_id
        self._strava_accessor: StravaAccessor = StravaAccessor(self._db, strava_credentials)

        google_auth: Optional[models.GoogleAuth] = crud.google_auth.get_for_user(self._db, self._user_id)
        if google_auth is None:
            error: str = f"Failed to process Strava notification for user: {self.notification.owner_id} " \
                         f"activity: {self.notification.object_id} due to missing Google Auth credentials."
            raise Exception(error)

        self._cal_accessor: GoogleCalendarAccessor = GoogleCalendarAccessor(db=self._db, google_auth=google_auth)

    def process(self):
        activity_template: Optional[models.CalendarTemplate] = crud.calendar_template.get_activity_template(self._db,
                                                                                                            self._user_id)
        if activity_template:
            self._process_activity_template(activity_template)

    def _process_activity_template(self, activity_template: models.CalendarTemplate):
        activity: Activity = self._strava_accessor.get_activity(self.notification.object_id)
        gen_title_template: str = calendar_template_utils.fill_template(activity_template.title_template, activity)
        gen_body_template: str = calendar_template_utils.fill_template(activity_template.body_template, activity)

        cal_event_id: str = self._cal_accessor.add_event(gen_title_template,
                                                         gen_body_template,
                                                         str(activity.timezone),
                                                         activity.start_date_local,
                                                         (activity.start_date_local + activity.moving_time),
                                                         False)
        logger.debug(f"Created new activity calendar event: {cal_event_id} "
                     f"for user: {self._user_id} and Strava activity: {activity}.")
