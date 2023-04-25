from datetime import datetime
from typing import Optional

from stravalib.model import Activity

from backend import schemas, crud, models
from backend.accessors import StravaAccessor, GoogleCalendarAccessor
from backend.core import logger
from backend.db.session import SessionLocal
from backend.models import StravaCredentials
from backend.models.calendar_template import CalendarTemplateType
from backend.utils import calendar_template_utils
from backend.utils.date_utils import beginning_of_day_in_utc, end_of_day_in_utc


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
        activity: Activity = self._strava_accessor.get_activity(self.notification.object_id)
        templates: [models.CalendarTemplate] = crud.calendar_template.get_all_active_templates(self._db,
                                                                                               self._user_id)
        if CalendarTemplateType.ACTIVITY_SUMMARY in templates.keys():
            template: models.CalendarTemplate = templates.pop(CalendarTemplateType.ACTIVITY_SUMMARY)
            self._process_activity_template(activity, template)

        for template_type, template in templates.items():
            self._process_summary_template(activity, template, template_type)

    def _process_activity_template(self, activity: Activity, activity_template: models.CalendarTemplate):
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

    def _process_summary_template(self, activity: Activity,
                                  activity_template: models.CalendarTemplate, summary_type: CalendarTemplateType):

        if summary_type == CalendarTemplateType.DAILY_SUMMARY:
            start_date: datetime = beginning_of_day_in_utc(activity.start_date_local)
            end_date: datetime = end_of_day_in_utc(activity.start_date_local)
            activities = self._strava_accessor.get_activities(start_date, end_date)
        elif summary_type == CalendarTemplateType.WEEKLY_SUMMARY:
            start_date: datetime = beginning_of_day_in_utc(activity.start_date_local)
            end_date: datetime = end_of_day_in_utc(activity.start_date_local)
            activities = self._strava_accessor.get_activities(start_date, end_date)
        else:
            raise Exception(f"Failed to process summary template for user: {self._user_id} due to "
                            f"invalid summary type: {summary_type}")

        gen_title_template: str = calendar_template_utils.fill_summary_template(activity_template.title_template, activities)
        gen_body_template: str = calendar_template_utils.fill_summary_template(activity_template.body_template, activities)

        cal_event_id: str = self._cal_accessor.add_event(gen_title_template,
                                                         gen_body_template,
                                                         str(activity.timezone),
                                                         start_date,
                                                         end_date,
                                                         True)

        logger.debug(f"Created new summary calendar event: {cal_event_id} "
                     f"for user: {self._user_id} and Strava activity: {activity}.")
