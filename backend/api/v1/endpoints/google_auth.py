import logging
import os

import google_auth_oauthlib.flow
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session


from backend import models, schemas, crud
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

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )

    return RedirectResponse(authorization_url)


@router.get('/callback', response_model=schemas.Msg)
def google_auth_callback(request: Request,
                         state: str,
                         db: Session = Depends(deps.get_db),
                         current_user: models.User = Depends(deps.get_current_active_user)):
    try:
        flow: google_auth_oauthlib.flow.Flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            GOOGLE_CONFIG_PATH,
            scopes=GOOGLE_CALENDAR_AUTH_SCOPES,
            state=state
        )
        flow.redirect_uri = settings.GOOGLE_AUTH_CALLBACK_URL

        # Fix localhost testing
        authorization_response = 'https://' + str(request.url).replace('http://', '').replace('https://', '')
        flow.fetch_token(authorization_response=authorization_response)
    except Exception as e:
        logging.error(f"Failed to authenticate user during Google auth request callback. {e}")
        raise HTTPException(status_code=403, detail="Failed to authenticate user during Google auth request callback.")

    google_credentials = flow.credentials

    google_auth: schemas.GoogleAuthCreate = schemas.GoogleAuthCreate(
        client_id=google_credentials.client_id,
        client_secret=google_credentials.client_secret,
        expiry=google_credentials.expiry,
        refresh_token=google_credentials.refresh_token,
        scopes=google_credentials.scopes
    )

    crud.google_auth.create_and_add_to_user(db, current_user.id, google_auth)

    return schemas.Msg(msg="Authenticated Google Auth")

