from fastapi import APIRouter, Request, HTTPException, Cookie
from fastapi.responses import RedirectResponse
from typing import Optional
from apiclient import discovery
import httplib2
from oauth2client import client
import json
import os

import google.oauth2.credentials
import google_auth_oauthlib.flow

from strava_calendar_summary_data_access_layer import User, UserController, StravaCredentials
from strava_calendar_summary_utils import StravaUtil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_CONFIG_PATH = os.path.join(ROOT_DIR, '../../client_secret.json')
GOOGLE_CALENDAR_AUTH_SCOPES = ['https://www.googleapis.com/auth/calendar.app.created']

router = APIRouter()


@router.get('/auth/googleCalendar')
async def google_calendar_auth(request: Request):
    # if not strava_access_token or not strava_refresh_token or not strava_token_expires_at:
    #     raise HTTPException(status_code=400, detail='Could not find strava_auth cookie when processing Google '
    #                                                 'Calendar auth. Please verify your strava account before '
    #                                                 'verifying your Google Calendar account.')

    # Exchange auth code for access token, refresh token, and ID token
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CONFIG_PATH,
        scopes=GOOGLE_CALENDAR_AUTH_SCOPES)

    print(request.url_for('google_calendar_auth_callback'))
    # flow.redirect_uri = 'localhost:8000/auth/google/calendar/verifyLogin'
    flow.redirect_uri = request.url_for('google_calendar_auth_callback')

    authorization_url, state = flow.authorization_url(
        access_type='offline'
    )

    request.session['google_auth_state'] = state
    return RedirectResponse(authorization_url)


@router.get('/auth/googleCalendar/callback')
async def google_calendar_auth_callback(request: Request):
    # try:
    #     body = await request.json()
    # except:
    #     raise HTTPException(status_code=400, detail='Missing required request body')
    #
    # if 'google_auth_code' not in body:
    #     raise HTTPException(status_code=400, detail='Missing required request parameters')
    #
    # code = body['google_auth_code']

    if 'strava_credentials' not in request.session:
        raise HTTPException(status_code=400, detail='Please authenticate with Strava before adding a Calendar')

    state = request.session['google_auth_state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CONFIG_PATH,
        scopes=GOOGLE_CALENDAR_AUTH_SCOPES,
        state=state
    )
    flow.redirect_uri = request.url_for('google_calendar_auth_callback')

    print(str(request.url))
    authorization_response = 'https://' + str(request.url).replace('http://', '')
    flow.fetch_token(authorization_response=authorization_response)

    google_credentials = flow.credentials
    request.session['google_credentials'] = json.loads(google_credentials.to_json())

    print(request.session['strava_credentials'])
    strava_creds = StravaCredentials.from_dict(request.session['strava_credentials'])
    strava_util = StravaUtil(strava_creds)

    user = User(str(strava_util.get_athlete_id()), strava_creds, google_credentials)
    UserController().insert(user.user_id, user)

    return RedirectResponse('http://localhost:5500/?stage=authorized')
