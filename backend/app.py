import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.db.session import SessionLocal
from backend.db.init_db import init_db
from backend.core.config import settings
from backend.api.v1.api import api_router

db = SessionLocal()
init_db(db)

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://localhost:*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
