from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend import models, crud
from backend.api import deps
from backend.models import MeMsg, UserRead

router = APIRouter()


# @router.post("/", response_model=schemas.User)
# def create_user(new_user: schemas.UserCreate, db: Session = Depends(deps.get_db)) -> Any:
#     """
#     Create a new user
#     """
#     user: Optional[models.User] = crud.user.get_by_email(db, new_user.email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="A user with this email already exists.",
#         )
#     user = crud.user.create(db, new_user)
#     account_verification_token: str = create_account_verification_token(new_user.email)
#     account_verification_link: str = f"{settings.API_HOST}/users/verify?token={account_verification_token}"
#     print(account_verification_link)
#     send_new_account_email(new_user.email, new_user.first_name, account_verification_link)
#     return user
#
#
# @router.post("/verify", response_model=schemas.Msg)
# def verify_user(token: str, db: Session = Depends(deps.get_db)) -> Any:
#     """
#     Verify a users account
#     """
#     email: Optional[str] = confirm_account_verification_token(token)
#     user: Optional[models.User] = None
#
#     if email:
#         temp_user: Optional[models.User] = crud.user.get_by_email(db, email)
#         user = temp_user if temp_user.status == models.UserStatus.PENDING_EMAIL_VERIFICATION else None
#
#     if not user:
#         # Show a generic message for failing to validate to reduce impact of brute force attacks
#         raise HTTPException(
#             status_code=400,
#             detail="This account doesn't exist, the validation token is incorrect, or the account is already verified.",
#         )
#
#     user.status = models.UserStatus.ACTIVE
#     crud.user.update(db, user, {
#         'status': models.UserStatus.ACTIVE
#     })
#
#     return {
#         "msg": "Account verified."
#     }


@router.get("/me", response_model=MeMsg)
def get_user_me(db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_active_user)):
    """
    Get current signed-in user
    """

    return {
        **current_user.dict(),
        'hasStravaAuth': crud.strava_credentials.user_has_strava_credentials(db=db, user_id=current_user.id),
        'hasGoogleCalendarAuth': crud.google_calendar_auth.user_has_google_calendar_auth(db=db, user_id=current_user.id)
    }
