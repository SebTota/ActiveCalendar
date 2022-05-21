from pydantic import BaseModel


class UserUI(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    strava_authenticated: bool
    calendar_authenticated: bool
