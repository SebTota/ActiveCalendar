from fastapi import FastAPI, APIRouter
from starlette.middleware.sessions import SessionMiddleware
import os

from backend.routers import google_calendar_auth, strava_auth, strava_webhook, summary_template_controller
from strava_calendar_summary_utils import Logging

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv('COOKIE_SECRET_KEY'))
app.include_router(google_calendar_auth.router, prefix='/api')
app.include_router(strava_webhook.router, prefix='/api')
app.include_router(strava_auth.router, prefix='/api')
app.include_router(summary_template_controller.router, prefix='/api')
Logging()


@app.get('/api/ping')
def root():
    return 'Success'
