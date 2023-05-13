from datetime import datetime, timezone
import logging

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from stravalib.client import Client

from backend import models, crud
from backend.api import deps
from backend.core.config import settings
from backend.models import Msg, StravaCredentialsCreate

router = APIRouter()


@router.get('/auth')
def strava_auth():
    auth_url = Client().authorization_url(
        client_id=int(settings.STRAVA_CLIENT_ID),
        redirect_uri=settings.STRAVA_AUTH_CALLBACK_URL,
        scope=['read', 'activity:read_all'])

    return RedirectResponse(auth_url + '&approval_prompt=auto')


@router.get('/callback', response_model=Msg)
def strava_auth_callback(code: str,
                         db: Session = Depends(deps.get_db),
                         current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        token_response = Client().exchange_code_for_token(
            client_id=int(settings.STRAVA_CLIENT_ID),
            client_secret=settings.STRAVA_CLIENT_SECRET,
            code=code)
    except:
        logging.error('Could not authenticate user with Strava. Strava exchange code for token failed.')
        raise HTTPException(status_code=400,
                            detail='The authorization code provided was invalid. '
                                   'Please try authenticating with Strava again')

    access_token: str = str(token_response['access_token'])
    refresh_token: str = token_response['refresh_token']
    expires_at: datetime = datetime.fromtimestamp(token_response['expires_at'], timezone.utc)

    client: Client = Client(access_token=access_token)
    athlete_id: int = int(client.get_athlete().id)

    if athlete_id is None or athlete_id < 0:
        logging.error(f'Could not find the athlete details: {athlete_id} during Strava authentication.')
        raise HTTPException(status_code=500,
                            detail='Failed to retrieve athlete details during authentication.')

    # TODO: Delete old auth credentials for this user if they exist

    strava_credentials: StravaCredentialsCreate = StravaCredentialsCreate(access_token=access_token,
                                                                          expires_at=expires_at,
                                                                          refresh_token=refresh_token,
                                                                          user_id=current_user.id)

    crud.strava_credentials.create_and_add_to_user(db=db, strava_user_id=athlete_id, obj=strava_credentials)

    return Msg(msg="Authenticated.")
