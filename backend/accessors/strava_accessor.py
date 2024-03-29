from datetime import datetime, timezone

import pytz
from sqlmodel import Session
from stravalib.client import Client
from stravalib.model import Athlete, Activity

from backend import crud
from backend.core import logger
from backend.core.config import settings
from backend.models import StravaCredentials


class StravaAccessor:
    def __init__(self, db: Session, strava_credentials: StravaCredentials):
        self._db: Session = db
        self._strava_credentials: StravaCredentials = strava_credentials
        self._init_strava_client()

    def _init_strava_client(self):
        self._client = Client()
        self._client.access_token = self._strava_credentials.access_token
        self._client.refresh_token = self._strava_credentials.refresh_token
        self._client.token_expires_at = self._strava_credentials.expires_at

    def _before_api_call(self) -> None:
        self._update_access_token_if_necessary()

    def _update_access_token_if_necessary(self) -> None:
        """
        Checks if we need to update the users Strava access token.
        """
        if datetime.now() > self._strava_credentials.expires_at:
            logger.debug(f"Current time: {datetime.now()}, creds expire at: {self._strava_credentials.expires_at}"
                         f" so refreshing token...")
            self._update_access_token()

    def _update_access_token(self):
        """
        Updates the users Strava access token using the refresh token, and updates the db with the new credentials.
        """
        refresh_response = self._client.refresh_access_token(
            client_id=int(settings.STRAVA_CLIENT_ID),
            client_secret=settings.STRAVA_CLIENT_SECRET,
            refresh_token=self._strava_credentials.refresh_token)

        self._strava_credentials.access_token = refresh_response['access_token']
        self._strava_credentials.refresh_token = refresh_response['refresh_token']
        self._strava_credentials.expires_at = datetime.fromtimestamp(refresh_response['expires_at'], timezone.utc)

        self._strava_credentials = crud.strava_credentials.update(db=self._db, obj=self._strava_credentials)
        self._init_strava_client()
        return self._strava_credentials

    def get_athlete_id(self) -> int:
        self._before_api_call()
        return self._client.get_athlete().id

    def get_athlete(self) -> Athlete:
        self._before_api_call()
        return self._client.get_athlete()

    def get_activities(self, after: datetime, before: datetime, limit: int = 20) -> [Activity]:
        self._before_api_call()
        activities: [Activity] = list(self._client.get_activities(before, after, limit))
        for activity in activities:
            activity.start_date_local = pytz.timezone(str(activity.timezone)).localize(activity.start_date_local)
        return activities

    def get_activity(self, activity_id) -> Activity:
        self._before_api_call()
        activity: Activity = self._client.get_activity(activity_id=activity_id)

        # Localize the start_date_local variable
        activity.start_date_local = pytz.timezone(str(activity.timezone)).localize(activity.start_date_local)
        return activity
