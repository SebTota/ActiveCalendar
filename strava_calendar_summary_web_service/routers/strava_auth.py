from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Cookie
from fastapi.responses import RedirectResponse
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from uuid import UUID, uuid4
from stravalib.client import Client
import logging
import os

from strava_calendar_summary_data_access_layer import StravaCredentials
from strava_calendar_summary_utils import StravaUtil
from strava_calendar_summary_web_service.models import SessionData

backend = InMemoryBackend[UUID, SessionData]()


cookie = SessionCookie(
    cookie_name='cookie',
    identifier='general_verifier',
    auto_error=True,
    secret_key='very_secret_key',
    cookie_params=CookieParameters()
)

router = APIRouter()


@router.get('/auth/strava')
def strava_get_authorization_token(request: Request):
    strava_client = Client()  # TODO: Move this to utils package
    auth_url = strava_client.authorization_url(
            client_id=int(os.getenv('STRAVA_CLIENT_ID')),
            redirect_uri=request.url_for('strava_authorized_callback'),
            scope=['activity:read_all'],)

    return RedirectResponse(auth_url)


@router.get('/auth/strava/callback')
def strava_authorized_callback(request: Request):
    if 'code' not in request.query_params:
        raise HTTPException(status_code=400, detail='Missing required request parameters')
    code = request.query_params['code']

    strava_client = Client()  # TODO: Move this to utils package

    try:
        token_response = strava_client.exchange_code_for_token(
            client_id=int(os.getenv('STRAVA_CLIENT_ID')), 
            client_secret=os.getenv('STRAVA_CLIENT_SECRET'), 
            code=code)
    except:
        logging.error('Could not authenticate user with Strava. Strava exchange code for token failed.')
        raise HTTPException(
            status_code=400, 
            detail='The authorization code provided was invalid. Please try authenticating with Strava again')

    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    expires_at = token_response['expires_at']

    request.session['strava_credentials'] = StravaCredentials(access_token, refresh_token, expires_at).to_dict()
    return RedirectResponse('http://localhost:5500/?stage=strava_authorized')
