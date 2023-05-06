from fastapi import APIRouter
from logging.config import dictConfig

from backend.core.log_config import LogConfig
from backend.api.v1.endpoints import users, strava_auth, google_auth, strava_webhook, calendar_templates

dictConfig(LogConfig().dict())

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(strava_auth.router, prefix='/strava', tags=["strava", "auth"])
api_router.include_router(strava_webhook.router, prefix='/strava', tags=["strava", "strava activity", "strava webhook"])
api_router.include_router(google_auth.router, prefix='/google', tags=["auth", "google"])
api_router.include_router(calendar_templates.router, prefix='/calendar_template', tags=["calendar", "template"])
