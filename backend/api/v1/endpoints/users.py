from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.api import deps
from backend.core.config import settings
from backend.core.security import create_account_verification_token, confirm_account_verification_token
from backend.utils.email_utils import send_new_account_email

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(deps.get_db)) -> Any:
    user: Optional[models.User] = crud.user.get_by_email(db, new_user.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )
    user = crud.user.create(db, new_user)
    account_verification_token: str = create_account_verification_token(new_user.email)
    account_verification_link: str = f"{settings.API_HOST}/users/verify?token={account_verification_token}"
    print(account_verification_link)
    send_new_account_email(new_user.email, new_user.first_name, account_verification_link)
    return user


@router.post("/verify", response_model=schemas.Msg)
def verify_user(token: str, db: Session = Depends(deps.get_db)) -> Any:
    email: Optional[str] = confirm_account_verification_token(token)
    user: Optional[models.User] = None

    if email:
        temp_user: Optional[models.User] = crud.user.get_by_email(db, email)
        user = temp_user if temp_user.status == models.UserStatus.PENDING_EMAIL_VERIFICATION else None

    if not user:
        # Show a generic message for failing to validate to reduce impact of brute force attacks
        raise HTTPException(
            status_code=400,
            detail="This account doesn't exist, the validation token is incorrect, or the account is already verified.",
        )

    user.status = models.UserStatus.ACTIVE
    crud.user.update(db, user, {
        'status': models.UserStatus.ACTIVE
    })

    return {
        "msg": "Account verified."
    }

