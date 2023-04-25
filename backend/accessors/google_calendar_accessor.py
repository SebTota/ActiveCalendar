from datetime import datetime, timedelta
from typing import Union

from sqlalchemy.orm import Session

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from backend.core import logger

from backend import schemas, crud
from backend.models import GoogleAuth

SCOPES = ['https://www.googleapis.com/auth/calendar.app.created',
          'https://www.googleapis.com/auth/calendar.calendarlist.readonly']
CALENDAR_NAME = 'Strava Summary'


class GoogleCalendarAccessor:
    def __init__(self, db: Session, google_auth: GoogleAuth) -> None:
        """
        Init GoogleCalendarAccessor for Google Calendar API Calls
        """
        self._db = db
        self._google_auth = google_auth

        self._refresh_creds_if_needed()
        self._service: build = build('calendar', 'v3', credentials=self._get_credentials())

        self._calendar_id = self._get_app_calendar_id(CALENDAR_NAME)
        if self._calendar_id is None:
            self._calendar_id = self._create_app_calendar(CALENDAR_NAME)

    def _get_credentials(self) -> Credentials:
        return Credentials(token=self._google_auth.token,
                           token_uri=self._google_auth.token_uri,
                           client_id=self._google_auth.client_id,
                           expiry=self._google_auth.expiry,
                           client_secret=self._google_auth.client_secret,
                           refresh_token=self._google_auth.refresh_token,
                           scopes=self._google_auth.scopes)

    def _before_each_request(self):
        self._refresh_creds_if_needed()

    def _refresh_creds_if_needed(self):
        creds: Credentials = self._get_credentials()
        if creds and creds.expiry < datetime.utcnow() + timedelta(minutes=15):
            logger.info(f"Refreshing Google credentials for user: {self._google_auth.user_id}.")
            creds.refresh(Request())
            changes: schemas.GoogleAuthUpdate = schemas.GoogleAuthUpdate(token=creds.token,
                                                                         token_uri=creds.token_uri,
                                                                         client_id=creds.client_id,
                                                                         client_secret=creds.client_secret,
                                                                         expiry=creds.expiry,
                                                                         refresh_token=creds.refresh_token,
                                                                         scopes=creds.scopes)
            self._google_auth = crud.google_auth.update(db=self._db, db_obj=self._google_auth, obj_in=changes)

    def _get_app_calendar_id(self, calendar_name) -> Union[str, None]:
        """
        Retrieve the id of a calendar with the specified name if one exists
        :param calendar_name: the name of the calendar to look for
        :return: the id of the calendar if one exists, or None if no match is found
        """
        self._before_each_request()

        page_token = None
        while True:
            calendars = self._service.calendarList().list(pageToken=page_token).execute()
            for calendar in calendars['items']:
                if calendar['summary'] == calendar_name:
                    print('found existing calendar')
                    return calendar['id']
            if not page_token:
                return None

    def _create_app_calendar(self, calendar_name) -> str:
        """
        Create a new calendar
        :param calendar_name: the name of the calendar
        :return: id of the calendar created
        """
        self._before_each_request()

        calendar = {
            'kind': 'calendar#calendar',
            'summary': calendar_name
        }

        created_calendar_id = self._service.calendars().insert(body=calendar).execute()['id']
        return created_calendar_id

    def add_all_day_event(self, name: str, description: str, timezone: str, date: str) -> str:
        """
        Add an all day calendar event
        :param name: name of the calendar event
        :param description: description of the calendar event
        :param timezone: timezone of where the event happened
        :param date: date of the event
        :return: the id of the calendar event or '-1' on error
        """
        return self.add_event(name, description, timezone, date, date)

    def update_all_day_event(self, event_id: str, name: str, description: str, timezone: str, date: str) -> str:
        """
        Update an all day calendar event
        :param event_id: the calendar event id that will be updated
        :param name: name of the calendar event
        :param description: description of the calendar event
        :param timezone: timezone of where the event happened
        :param date: date of the event
        :return: the id of the calendar event or '-1' on error
        """
        return self.update_event(event_id, name, description, timezone, date, date)

    def add_event(self, name: str, description: str, timezone: str, start_date: datetime, end_date: datetime, is_all_day_event: bool) -> str:
        """
        Add a new calendar event
        :return: the id of the calendar event or '-1' on error
        """
        self._before_each_request()
        event_body = {
            'summary': name,
            'description': description,
            'start': {
                'timeZone': timezone
            },
            'end': {
                'timeZone': timezone
            }
        }

        if is_all_day_event:
            event_body['start']['date'] = start_date.strftime('%Y-%m-%d')
            event_body['end']['date'] = end_date.strftime('%Y-%m-%d')
        else:
            event_body['start']['dateTime'] = start_date.strftime('%Y-%m-%dT%H:%M:%S')
            event_body['end']['dateTime'] = end_date.strftime('%Y-%m-%dT%H:%M:%S')

        event = self._service.events().insert(calendarId=self._calendar_id, body=event_body).execute()
        return event.get('id')

    def update_event(self, event_id: str, name: str, description: str, timezone: str, start: str, end: str) -> str:
        """
        Update a calendar event for the signed in user
        :param event_id: the id of the calendar event to update
        :param name: new name of the calendar event
        :param description: new description of the calendar event
        :param timezone: new timezone of where the event happened
        :param start: new start datetime of the event
        :param end: new end datetime of the event
        :return: the id of the calendar event or '-1' on error
        """
        self._before_each_request()
        event_body = {
            'summary': name,
            'description': description,
            'start': {
                'timeZone': timezone
            },
            'end': {
                'timeZone': timezone
            }
        }

        if len(start) == 10 and len(end) == 10:
            event_body['start']['date'] = start
            event_body['end']['date'] = end
        elif len(start) == 19 and len(end) == 19:
            event_body['start']['dateTime'] = start
            event_body['end']['dateTime'] = end
        else:
            return '-1'

        event = self._service.events().update(calendarId=self._calendar_id, eventId=event_id, body=event_body).execute()
        return event.get('id')

    def delete_event(self, event_id):
        """
        Delete a calendar event
        :param event_id: calendar event id that represents the event that should be deleted
        :return: none
        """
        self._before_each_request()
        self._service.events().delete(calendarId=self._calendar_id, eventId=event_id).execute()
