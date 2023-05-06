from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.db.init_db import init_db
from backend.core.config import settings
from backend.api.v1.api import api_router

init_db()

app = FastAPI(openapi_url="/api/v1/openapi.json")

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://localhost:*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
