from strava_calendar_summary_data_access_layer import StravaCredentials, User, UserController
from stravalib.client import Client
from stravalib.model import Athlete, Activity

from typing import List
import time
import os


class StravaAccessor:
    def __init__(self, strava_credentials: StravaCredentials, user: User = None):
        """Init StravaAccessor
        strava_credentials: The Strava Credentials object used to authenticate all API calls
        user: The User object of the requesting user. If present, will update refresh token in db if needed
        """
        self._strava_credentials: StravaCredentials = strava_credentials
        self._user: User = user
        self._init_strava_client()
        
    def _init_strava_client(self):
        self._client = Client()
        self._client.access_token = self._strava_credentials.access_token
        self._client.refresh_token = self._strava_credentials.refresh_token
        self._client.token_expires_at = self._strava_credentials.expiry_date

    def _before_api_call(self) -> None:
        self._update_access_token_if_necessary()

    def _update_access_token_if_necessary(self) -> None:
        if time.time() > self._client.token_expires_at:
            self.update_strava_credentials()

    def update_strava_credentials(self) -> StravaCredentials:
        refresh_response = self._client.refresh_access_token(
            client_id=int(os.getenv('STRAVA_CLIENT_ID')),
            client_secret=os.getenv('STRAVA_CLIENT_SECRET'),
            refresh_token=self._client.refresh_token)

        self._strava_credentials.access_token = refresh_response['access_token']
        self._strava_credentials.refresh_token = refresh_response['refresh_token']
        self._strava_credentials.expiry_date = refresh_response['expires_at']

        if self._user is not None:
            self._user.strava_credentials = self._strava_credentials
            UserController().update(self._user.user_id, self._user)

        return self._strava_credentials

    def get_athlete_id(self) -> int:
        self._before_api_call()
        return self._client.get_athlete().id

    def get_athlete(self) -> Athlete:
        self._before_api_call()
        return self._client.get_athlete()

    def get_activities(self, before=None, after=None, limit=None):
        self._before_api_call()
        return self._client.get_activities(before, after, limit)

    def get_activity(self, activity_id) -> Activity:
        self._before_api_call()
        return self._client.get_activity(activity_id=activity_id)
