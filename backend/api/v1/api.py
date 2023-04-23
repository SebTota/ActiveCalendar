from fastapi import APIRouter
from logging.config import dictConfig

from backend.core.log_config import LogConfig
from backend.api.v1.endpoints import login, users, strava_auth, strava_webhook, google_auth

dictConfig(LogConfig().dict())

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login", "auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(strava_auth.router, prefix='/strava', tags=["strava", "auth"])
api_router.include_router(strava_webhook.router, prefix='/strava', tags=["strava", "strava activity", "strava webhook"])
api_router.include_router(google_auth.router, prefix='/google', tags=["auth", "google"])
