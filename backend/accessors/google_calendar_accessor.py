from typing import Union

from strava_calendar_summary_data_access_layer import User, UserController

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import logging

SCOPES = ['https://www.googleapis.com/auth/calendar.app.created',
          'https://www.googleapis.com/auth/calendar.calendarlist.readonly']
CALENDAR_NAME = 'Strava Summary'


class GoogleCalendarAccessor:
    def __init__(self, calendar_credentials: Credentials, calendar_id: str = None, user: User = None):
        """Init GoogleCalendarAccessor for Google Calendar API Calls
        calendar_credentials: the credentials to authenticate each API call with
        calendar_id: the id of the calendar created for this application IF one exists
        user: the User object of the requesting user. If present, updates calendar_credentials on refresh of credentials
        """
        self._calendar_auth = calendar_credentials
        self._calendar_id = calendar_id
        self._user = user

        self._refresh_creds_if_needed()
        self._service: build = build('calendar', 'v3', credentials=self._calendar_auth)

        if self._calendar_id is None:
            self._calendar_id = self._get_app_calendar_id(CALENDAR_NAME)
            if self._calendar_id is None:
                self._calendar_id = self._create_app_calendar(CALENDAR_NAME)
            self._save_app_calendar_id(self._calendar_id)

    def get_calendar_id(self) -> Union[str, None]:
        """
        Retrieve the application's calendar id
        :return: the calendar id or None if one doesn't yet exist
        """
        return self._calendar_id

    def _before_each_request(self):
        self._refresh_creds_if_needed()

    def _refresh_creds_if_needed(self):
        if self._calendar_auth and self._calendar_auth.refresh_token:
            self._calendar_auth.refresh(Request())

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

    def _save_app_calendar_id(self, calendar_id: str):
        """
        Save the calendar id to the signed in user
        :param calendar_id: the id of the calendar
        :return: none
        """
        if self._user is not None and self._user.calendar_id != calendar_id:
            self._user.calendar_id = calendar_id
            UserController().update(self._user.user_id, self._user)
            logging.info('Saved app calendar: {} for user: {}'.format(calendar_id, self._user.user_id))

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

    def add_event(self, name: str, description: str, timezone: str, start: str, end: str) -> str:
        """
        Add a new calendar event
        :param name: name of the calendar event
        :param description: description of the calendar event
        :param timezone: timezone of where the event happened
        :param start: start datetime of the event
        :param end: end datetime of the event
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
