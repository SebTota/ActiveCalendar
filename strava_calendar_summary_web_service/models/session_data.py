from pydantic import BaseModel


class SessionData(BaseModel):
    strava_credentials: dict
    google_auth_state: dict
    google_credentials: dict
