import os

import google_auth_oauthlib.flow
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session


from backend import models
from backend.api import deps
from backend.core.config import settings
from backend.accessors.google_calendar_accessor import SCOPES as GOOGLE_CALENDAR_AUTH_SCOPES


router = APIRouter()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_CONFIG_PATH = os.path.join(ROOT_DIR, '../../../client_secret.json')


@router.get('/auth')
def google_auth(db: Session = Depends(deps.get_db),
                current_user: models.User = Depends(deps.get_current_active_user)):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CONFIG_PATH,
        scopes=GOOGLE_CALENDAR_AUTH_SCOPES)
    flow.redirect_uri = settings.GOOGLE_AUTH_CALLBACK_URL
    print(settings.GOOGLE_AUTH_CALLBACK_URL)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )

    return RedirectResponse(authorization_url)


@router.get('/callback')
def google_auth_callback(request: Request,
                         state: str,
                         db: Session = Depends(deps.get_db),
                         current_user: models.User = Depends(deps.get_current_active_user)):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        GOOGLE_CONFIG_PATH,
        scopes=GOOGLE_CALENDAR_AUTH_SCOPES,
        state=state
    )
    flow.redirect_uri = settings.GOOGLE_AUTH_CALLBACK_URL

    # Fix localhost testing
    authorization_response = 'https://' + str(request.url).replace('http://', '').replace('https://', '')
    flow.fetch_token(authorization_response=authorization_response)

    google_credentials = flow.credentials

    return google_credentials

