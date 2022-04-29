from strava_calendar_summary_data_access_layer import StravaEvent
from strava_calendar_summary_utils import StravaEventMiddleware

from fastapi import APIRouter, Request, HTTPException
import os
import logging

router = APIRouter()


@router.get('/webhook')
def get_webhook(request: Request):
    params = request.query_params
    if 'hub.mode' not in params or 'hub.verify_token' not in params or 'hub.challenge' not in params:
        raise HTTPException(status_code=400, detail='Missing required request parameters')

    hub_mode = params['hub.mode']
    hub_verification_token = params['hub.verify_token']
    hub_challenge = params['hub.challenge']

    if hub_mode == 'subscribe' and hub_verification_token == os.getenv('STRAVA_WEBHOOK_VERIFICATION_TOKEN'):
        print('Webhook verified')
        return {'hub.challenge': hub_challenge}
    else:
        raise HTTPException(status_code=403, detail='Webhook could not be verified')


@router.post('/webhook')
async def post_webhook(request: Request):
    body = await request.json()

    if 'subscription_id' not in body or 'object_type' not in body or 'aspect_type' not in body \
        or 'owner_id' not in body or 'object_id' not in body or 'event_time' not in body:
        raise HTTPException(status_code=400, detail='Missing required request parameters')

    subscription_id = body['subscription_id']

    if int(subscription_id) != int(os.getenv('STRAVA_SUBSCRIPTION_ID')):
        raise HTTPException(status_code=400, detail='Invalid subscription id')

    object_type = body['object_type']  # activity, athlete
    aspect_type = body['aspect_type']  ## create, update, delete
    user_id = body['owner_id']
    activity_id = body['object_id']
    event_time = body['event_time']

    try:
        updates = body['updates']
    except:
        updates = None

    new_event: StravaEvent = StravaEvent(object_type, activity_id, aspect_type, updates, user_id, event_time)

    # Ignore none 'activity' events
    if object_type != 'activity':
        logging.info('Skipping "{}" activity: {} for user: {}'.format(object_type, activity_id, user_id))
        return {}

    logging.info('Received a new "{}" activity: {} event for user: {}'.format(
        aspect_type, activity_id, user_id))

    try:
        message_id = StravaEventMiddleware().publish_strava_event(new_event)
        logging.info("Published message: {} for strava event id: {} for user: {} to event middleware.".format(message_id, activity_id, user_id))
    except Exception as err:
        logging.error('Failed to publish strava event id: {} for user: {} to the event middleware. Error: {}', activity_id, user_id, err)
