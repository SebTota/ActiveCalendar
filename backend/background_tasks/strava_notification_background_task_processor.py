from typing import Optional

from stravalib.model import Activity

from backend import schemas, crud, models
from backend.accessors import StravaAccessor, GoogleCalendarAccessor
from backend.core import logger
from backend.db.session import SessionLocal
from backend.models import StravaCredentials
from backend.schemas import CalendarTemplateType
from backend.utils import calendar_template_utils


class StravaNotificationBackgroundTaskProcessor:

    def __init__(self):
        self._db: SessionLocal = SessionLocal()

    def process(self, notification: schemas.StravaNotification):
        strava_credentials: Optional[StravaCredentials] = crud.strava_credentials.get(self._db, notification.owner_id)
        if strava_credentials is None:
            logger.error(f"Failed to process Strava notification for user: {notification.owner_id} "
                         f"activity: {notification.object_id} because the user has not authed with Strava")
            return

        strava_accessor: StravaAccessor = StravaAccessor(self._db, strava_credentials)
        activity: Activity = strava_accessor.get_activity(notification.object_id)
        templates: dict = crud.calendar_template.get_all_active_templates(self._db, strava_credentials.user_id)

        if CalendarTemplateType.ACTIVITY_SUMMARY in templates.keys():
            # Generate activity summary for single activity
            template: models.CalendarTemplate = templates.pop(CalendarTemplateType.ACTIVITY_SUMMARY)
            gen_title_template: str = calendar_template_utils.fill_template(template.title_template, activity)
            gen_body_template: str = calendar_template_utils.fill_template(template.body_template, activity)
            print('Activity Summary')
            print(f'Title template: {gen_title_template}')
            print(f'Body template: {gen_body_template}')

        for template_type, template in templates.items():
            # If there was a regular activity_summary template type, it won't be in this list. This will
            # only contain summary templates.
            gen_title_template: str = calendar_template_utils.fill_template(template.title_template, activity)
            gen_body_template: str = calendar_template_utils.fill_template(template.body_template, activity)
            print('Other Summary')
            print(f'Title template: {gen_title_template}')
            print(f'Body template: {gen_body_template}')

        google_auth: Optional[models.GoogleAuth] = crud.google_auth.get_for_user(self._db, strava_credentials.user_id)
        if not google_auth:
            logger.error(f"Could not process Strava event: {notification.object_id} "
                         f"for user: {strava_credentials.user_id} due to missing Google Auth.")
            return

        cal_accessor: GoogleCalendarAccessor = GoogleCalendarAccessor(db=self._db, google_auth=google_auth)


strava_notification_background_task_processor: StravaNotificationBackgroundTaskProcessor = \
    StravaNotificationBackgroundTaskProcessor()
