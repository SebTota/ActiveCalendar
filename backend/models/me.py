from pydantic import BaseModel

from backend.models import UserStatus


class MeMsg(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    status: UserStatus
    is_superuser: bool
    hasStravaAuth: bool
    hasGoogleCalendarAuth: bool
