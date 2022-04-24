from fastapi import FastAPI

from routers import strava_webhook

app = FastAPI()
app.include_router(strava_webhook.router)

@app.get('/')
def root():
  return 'Success'
