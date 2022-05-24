from backend.models import user_auth
from strava_calendar_summary_data_access_layer import User, UserController

from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Cookie
from fastapi.responses import RedirectResponse
import os
import google_auth_oauthlib.flow


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_CONFIG_PATH = os.path.join(ROOT_DIR, '../../client_secret.json')
GOOGLE_CALENDAR_AUTH_SCOPES = ['https://www.googleapis.com/auth/calendar.app.created']

router = APIRouter()


@router.get('/auth/googleCalendar')
async def google_calendar_auth(request: Request, Authentication: Optional[str] = Cookie(None)):
    if Authentication is None:
        raise HTTPException(status_code=401, detail='User not signed in')

    # Exchange auth code for access token, refresh token, and ID token
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CONFIG_PATH,
        scopes=GOOGLE_CALENDAR_AUTH_SCOPES)

    flow.redirect_uri = request.url_for('google_calendar_auth_callback')
    authorization_url, state = flow.authorization_url(
        access_type='offline'
    )

    request.session['google_auth_state'] = state
    return RedirectResponse(authorization_url)


@router.get('/auth/googleCalendar/callback')
async def google_calendar_auth_callback(request: Request, Authentication: Optional[str] = Cookie(None)):
    if Authentication is None:
        raise HTTPException(status_code=401, detail='User not signed in')

    auth_cookie: user_auth.UserAuth = user_auth.decrypt_session_cookie(Authentication)

    if 'google_auth_state' not in request.session:
        raise HTTPException(status_code=400, detail='Please authenticate with Google Calendar')

    state = request.session['google_auth_state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CONFIG_PATH,
        scopes=GOOGLE_CALENDAR_AUTH_SCOPES,
        state=state
    )
    flow.redirect_uri = request.url_for('google_calendar_auth_callback')

    authorization_response = 'https://' + str(request.url).replace('http://', '').replace('https://', '')
    flow.fetch_token(authorization_response=authorization_response)

    google_credentials = flow.credentials

    user_controller: UserController = UserController()
    user: User = user_controller.get_by_id(auth_cookie.user_id)
    user.calendar_credentials = google_credentials
    UserController().update(user.user_id, user)
    return RedirectResponse(os.getenv('UI_BASE_URL'))
