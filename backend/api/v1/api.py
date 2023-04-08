from fastapi import APIRouter

from backend.api.v1.endpoints import login

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])