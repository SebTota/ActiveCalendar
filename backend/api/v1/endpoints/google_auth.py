import os
from typing import Optional

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests

from backend import models, crud
from backend.api import deps
from backend.core import logger, security
from backend.core.config import settings
from backend.accessors.google_calendar_accessor import SCOPES as GOOGLE_CALENDAR_AUTH_SCOPES
from backend.models import GoogleCalendarCredentials, GoogleCalendarCredentialsCreate, Msg, User, AuthProvider, \
    UserCreate, UserStatus, Token

router = APIRouter()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_CONFIG_PATH = os.path.join(ROOT_DIR, '../../../client_secret.json')

GOOGLE_OAUTH_USER_SCOPES: [str] = ['https://www.googleapis.com/auth/userinfo.email',
                                   'https://www.googleapis.com/auth/userinfo.profile',
                                   'openid']


@router.get('/auth')
async def google_user_auth():
    flow = Flow.from_client_secrets_file(
        GOOGLE_CONFIG_PATH,
        scopes=GOOGLE_OAUTH_USER_SCOPES)
    flow.redirect_uri = settings.GOOGLE_OAUTH_CALLBACK_URL

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )

    return RedirectResponse(authorization_url)


@router.get('/callback', response_model=Token)
async def google_user_auth_callback(state: str, code: str, db: Session = Depends(deps.get_db)):
    try:
        flow: Flow = Flow.from_client_secrets_file(
            GOOGLE_CONFIG_PATH,
            scopes=GOOGLE_OAUTH_USER_SCOPES,
            state=state
        )
        flow.redirect_uri = settings.GOOGLE_OAUTH_CALLBACK_URL
        flow.fetch_token(code=code)
    except Exception as e:
        logger.error(f"Failed to authenticate user during Google auth request callback. {e}")
        raise HTTPException(status_code=403, detail="Failed to authenticate user during Google auth request callback.")

    google_credentials = flow.credentials
    jwt_id_token: str = google_credentials.id_token
    user_id_token: {} = id_token.verify_oauth2_token(jwt_id_token,
                                                     requests.Request(),
                                                     settings.GOOGLE_OAUTH_CLIENT_ID,
                                                     clock_skew_in_seconds=10)

    is_verified: bool = bool(user_id_token['email_verified'])
    google_email: str = user_id_token['email']
    google_name: str = user_id_token['name']
    google_user_id: str = user_id_token['sub']

    if not is_verified:
        raise HTTPException(status_code=400, detail="Please use a verified Google account to sign in.")

    # If user exists, sign in. Else, sign up.
    user: Optional[User] = crud.crud_user.get_by_email(db=db, email=google_email)
    if not user:
        # User sign up
        logger.info(f"Creating new user with email: {google_email}.")
        first_name: str = google_name.split(' ')[0]
        last_name: str = ' '.join(google_name.split(' ')[1:])

        new_user: UserCreate = UserCreate(first_name=first_name,
                                          last_name=last_name,
                                          email=google_email,
                                          auth_provider=AuthProvider.GOOGLE,
                                          auth_provider_id=google_user_id,
                                          status=UserStatus.ACTIVE)

        user = crud.crud_user.create_user(db=db, obj=new_user)
        if not user:
            logger.error("Failed to save user information in db.")
            raise HTTPException(status_code=500, detail="Failed to create user.")

        # Create default calendar templates for new user
        crud.crud_calendar_template.create_default_templates_for_new_user(db=db, user_id=user.id)
    else:
        # User sign in
        if user.auth_provider != AuthProvider.GOOGLE:
            logger.info(f"User: {user.id} tried to sign in with Google, but has an account with another provider.")
            raise HTTPException(status_code=400,
                                detail="An account with this email already exists with a different provider.")

        if user.auth_provider_id != google_user_id:
            logger.error("User signed in with Google and the emails match, but 'sub' value is different.")
            raise HTTPException(status_code=400,
                                detail="Failed to validate Google account.")

    return security.create_auth_token(user)


@router.get('/calendar/auth')
def google_calendar_auth():
    flow = Flow.from_client_secrets_file(
        GOOGLE_CONFIG_PATH,
        scopes=GOOGLE_CALENDAR_AUTH_SCOPES)
    flow.redirect_uri = settings.GOOGLE_CALENDAR_AUTH_CALLBACK_URL

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )

    return RedirectResponse(authorization_url)


@router.get('/calendar/callback', response_model=Msg)
def google_calendar_auth_callback(state: str,
                                  code: str,
                                  db: Session = Depends(deps.get_db),
                                  current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        flow: Flow = Flow.from_client_secrets_file(
            GOOGLE_CONFIG_PATH,
            scopes=GOOGLE_CALENDAR_AUTH_SCOPES,
            state=state
        )
        flow.redirect_uri = settings.GOOGLE_CALENDAR_AUTH_CALLBACK_URL
        flow.fetch_token(code=code)
    except Exception as e:
        logger.error(f"Failed to authenticate user during Google Calendar auth request callback. {e}")
        raise HTTPException(status_code=403, detail="Failed to authenticate user during Google Calendar auth request callback.")

    existing_auth: Optional[GoogleCalendarCredentials] = crud.google_calendar_auth.get_for_user(db=db, user_id=current_user.id)
    if existing_auth:
        logger.debug(f"Removing Google Calendar auth for user: {current_user.id} because user is trying to "
                     f"re-authenticate with Google.")
        crud.google_calendar_auth.remove(db=db, obj=existing_auth)

    google_credentials = flow.credentials
    google_auth_create: GoogleCalendarCredentialsCreate = GoogleCalendarCredentialsCreate(
        token=google_credentials.token,
        expiry=google_credentials.expiry,
        refresh_token=google_credentials.refresh_token,
        scopes=google_credentials.scopes,
        user_id=current_user.id
    )

    crud.google_calendar_auth.create(db=db, obj=google_auth_create)
    return Msg(msg="Authenticated")
