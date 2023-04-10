from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend import schemas, crud, models
from backend.api import deps
from backend.core import security

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # username = email in this case
    user = crud.user.authenticate(db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        if crud.user.is_pending_email_verification(user):
            raise HTTPException(status_code=400, detail="Please verify your account through the email "
                                                        "sent to you before signing in.")
        else:
            raise HTTPException(status_code=400, detail="Inactive user")

    return security.create_auth_token(user)


@router.get("/me", response_model=schemas.User)
def get_me(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user
