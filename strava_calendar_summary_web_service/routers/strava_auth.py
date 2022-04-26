from fastapi import APIRouter, Request, HTTPException, Cookie
from typing import Optional

from fastapi.responses import RedirectResponse
from stravalib.client import Client
import logging
import os

from strava_calendar_summary_data_access_layer import User, UserController, StravaAuth
from strava_calendar_summary_utils import StravaUtil

router = APIRouter()


# This route should never really be needed since the auth URL never changes and is hard coded
@router.get('/auth/strava/getAuthorizationToken')
def strava_get_authorization_token():
    strava_client = Client()  # TODO: Move this to utils package
    return {
        'strava_client_id': strava_client.authorization_url(
            client_id=int(os.getenv('STRAVA_CLIENT_ID')), 
            redirect_uri=os.getenv('STRAVA_REDIRECT_URI'),
            scope='activity:read_all')
    }


@router.get('/auth/strava/authorized')
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

    response = RedirectResponse('http://localhost:5500/StravaCalendarSummaryWebsite/?stage=strava_authorized')

    response.set_cookie('strava_access_token', access_token)
    response.set_cookie('strava_refresh_token', refresh_token)
    response.set_cookie('strava_token_expires_at', expires_at)
    return response
