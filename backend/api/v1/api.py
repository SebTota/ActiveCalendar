from fastapi import APIRouter

from backend.api.v1.endpoints import login, users, strava

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(strava.router, prefix='/strava', tags=["strava"])
