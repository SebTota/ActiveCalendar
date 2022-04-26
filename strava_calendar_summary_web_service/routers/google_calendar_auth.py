from fastapi import APIRouter, Request, HTTPException, Cookie
from typing import Optional
from apiclient import discovery
import httplib2
from oauth2client import client
import json
import os

from strava_calendar_summary_data_access_layer import User, UserController, StravaAuth
from strava_calendar_summary_utils import StravaUtil


router = APIRouter()

CLIENT_SECRET_FILE_PATH = '/Users/sebastiantota/Documents/Projects/StravaCalendarSummary/StravaCalendarSummaryWebService/strava_calendar_summary_web_service/client_secret.json'

@router.post('/auth/googleCalendar/login')
async def google_calendar_login_auth(request: Request, strava_access_token: Optional[str] = Cookie(None), strava_refresh_token: Optional[str] = Cookie(None), strava_token_expires_at: Optional[int] = Cookie(None)):
    if not strava_access_token or not strava_refresh_token or not strava_token_expires_at:
        raise HTTPException(status_code=400, detail='Could not find strava_auth cookie when processing Google Calendar auth. \
            Please verify your strava account before verifying your Google Calendar account.')

    strava_credentials = StravaAuth(strava_access_token, strava_refresh_token, strava_token_expires_at)
    try:
        body = await request.json()
    except:
        raise HTTPException(status_code=400, detail='Missing required request body')

    if not request.headers.get('X-Requested-With'):
        raise HTTPException(status_code=403, detail='Webhook could not be verified')

    if 'google_auth_code' not in body:
        raise HTTPException(status_code=400, detail='Missing required request parameters')

    code = body['google_auth_code']

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_code(
        client_id = os.getenv('GOOGLE_CLIENT_ID'),
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET'),
        scope = ['https://www.googleapis.com/auth/calendar.app.created', 'profile', 'email'],
        code = code
    )

    # TODO: There has to be a better way to structure the StravaUtils class to not have to do this
    # OR maybe the user id should not be the strava ID and we should have that mapping elsewhere
    user: User = User(None, strava_credentials, credentials)

    strava_util = StravaUtil(user)
    user.id = strava_util.get_athlete().id
    user: User = UserController().insert(user.id, user)

    return 'success'