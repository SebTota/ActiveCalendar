import os
from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests

from backend import models, schemas, crud
from backend.api import deps
from backend.core import logger
from backend.core.config import settings
from backend.accessors.google_calendar_accessor import SCOPES as GOOGLE_CALENDAR_AUTH_SCOPES
from backend.models import GoogleAuth

router = APIRouter()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_CONFIG_PATH = os.path.join(ROOT_DIR, '../../../client_secret.json')

GOOGLE_OAUTH_USER_SCOPES: [str] = ['https://www.googleapis.com/auth/userinfo.email',
                                   'https://www.googleapis.com/auth/userinfo.profile',
                                   'openid']


@router.get('/auth')
def google_user_auth():
    flow = Flow.from_client_secrets_file(
        GOOGLE_CONFIG_PATH,
        scopes=GOOGLE_OAUTH_USER_SCOPES)
    flow.redirect_uri = settings.GOOGLE_OAUTH_CALLBACK_URL

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )

    return RedirectResponse(authorization_url)


@router.get('/callback')
def google_user_auth_callback(request: Request, state: str, db: Session = Depends(deps.get_db)):
    try:
        flow: Flow = Flow.from_client_secrets_file(
            GOOGLE_CONFIG_PATH,
            scopes=GOOGLE_OAUTH_USER_SCOPES,
            state=state
        )
        flow.redirect_uri = settings.GOOGLE_OAUTH_CALLBACK_URL

        # Fix localhost testing
        authorization_response = 'https://' + str(request.url).replace('http://', '').replace('https://', '')
        flow.fetch_token(authorization_response=authorization_response)
    except Exception as e:
        logger.error(f"Failed to authenticate user during Google auth request callback. {e}")
        # TODO Rather than raising an exception here, we need to redirect the user to the webapp and show an
        #    error there.
        raise HTTPException(status_code=403, detail="Failed to authenticate user during Google auth request callback.")

    google_credentials = flow.credentials
    jwt_id_token: str = google_credentials.id_token
    user_id_token: {} = id_token.verify_oauth2_token(jwt_id_token,
                                                     requests.Request(),
                                                     settings.GOOGLE_OAUTH_CLIENT_ID,
                                                     clock_skew_in_seconds=10)

    logger.info(user_id_token)
    is_verified: bool = bool(user_id_token['user_id_token'])

    # if not is_verified:
    # TODO Rather than raising an exception here, we need to redirect the user to the webapp and show an
    #    error there.

    user_email: str = user_id_token['email']
    name: str = user_id_token['name']

    first_name: str = name.split(' ')[0]
    last_name: str = ' '.join(name.split(' ')[1:])

    # TODO Check to make sure the user email doesn't already exist with another auth provider

    return schemas.Msg(msg="Authenticated Google Auth")


@router.get('/calendar/auth')
def google_calendar_auth(current_user: models.User = Depends(deps.get_current_active_user)):
    flow = Flow.from_client_secrets_file(
        GOOGLE_CONFIG_PATH,
        scopes=GOOGLE_CALENDAR_AUTH_SCOPES)
    flow.redirect_uri = settings.GOOGLE_CALENDAR_AUTH_CALLBACK_URL

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )

    return RedirectResponse(authorization_url)


@router.get('/calendar/callback', response_model=schemas.Msg)
def google_calendar_auth_callback(request: Request,
                                  state: str,
                                  db: Session = Depends(deps.get_db),
                                  current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        flow: Flow = Flow.from_client_secrets_file(
            GOOGLE_CONFIG_PATH,
            scopes=GOOGLE_CALENDAR_AUTH_SCOPES,
            state=state
        )
        flow.redirect_uri = settings.GOOGLE_AUTH_CALLBACK_URL

        # Fix localhost testing
        authorization_response = 'https://' + str(request.url).replace('http://', '').replace('https://', '')
        flow.fetch_token(authorization_response=authorization_response)
    except Exception as e:
        # TODO Rather than raising an exception here, we need to redirect the user to the webapp and show an
        #    error there.
        logger.error(f"Failed to authenticate user during Google Calendar auth request callback. {e}")
        raise HTTPException(status_code=403,
                            detail="Failed to authenticate user during Google Calendar auth request callback.")

    existing_auth: Optional[GoogleAuth] = crud.google_auth.get_for_user(current_user.id)
    if existing_auth:
        logger.debug(f"Removing Google Calendar auth for user: {current_user.id} because user is trying to "
                     f"re-authenticate with Google.")
        crud.google_auth.remove(db=db, id=existing_auth.id)

    google_credentials = flow.credentials
    google_auth_create: schemas.GoogleAuthCreate = schemas.GoogleAuthCreate(
        token=google_credentials.token,
        expiry=google_credentials.expiry,
        refresh_token=google_credentials.refresh_token,
        scopes=google_credentials.scopes
    )

    crud.google_auth.create_and_add_to_user(db, current_user.id, google_auth_create)

    return schemas.Msg(msg="Authenticated Google Calendar Auth")
