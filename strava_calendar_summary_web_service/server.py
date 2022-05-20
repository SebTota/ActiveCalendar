from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import os

from strava_calendar_summary_web_service.routers import strava_webhook, strava_auth, google_calendar_auth
from strava_calendar_summary_utils import Logging

app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(SessionMiddleware, secret_key=os.getenv('COOKIE_SECRET_KEY'))
app.include_router(google_calendar_auth.router)
app.include_router(strava_webhook.router)
app.include_router(strava_auth.router)
Logging()

origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
  return 'Success'
