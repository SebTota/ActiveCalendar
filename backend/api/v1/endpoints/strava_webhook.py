from datetime import datetime, timezone

from fastapi import APIRouter, Request, HTTPException

from backend import schemas
from backend.core import logger
from backend.core.config import settings

router = APIRouter()


@router.get('/webhook')
def subscribe_webhook(request: Request):
    params = request.query_params
    if 'hub.mode' not in params or 'hub.verify_token' not in params or 'hub.challenge' not in params:
        logger.error('Failed registering webhook due to missing request parameters.')
        raise HTTPException(status_code=400, detail='Missing required request parameters')

    hub_mode = params['hub.mode']
    hub_verification_token = params['hub.verify_token']
    hub_challenge = params['hub.challenge']

    if hub_mode == 'subscribe' and hub_verification_token == settings.STRAVA_WEBHOOK_VERIFICATION_TOKEN:
        logger.info('Webhook verified')
        return {'hub.challenge': hub_challenge}
    else:
        logger.error('Webhook registry request could not be verified due to hub.verify_token being incorrect. Strava '
                     'hub.verification_token: "{}" with hub.mode: "{}".'.format(hub_verification_token, hub_mode))
        raise HTTPException(status_code=403, detail='Webhook could not be verified')


@router.post('/webhook', status_code=201)
async def get_activity_webhook(request: Request):
    body = await request.json()

    if 'subscription_id' not in body or 'object_type' not in body or 'aspect_type' not in body \
            or 'owner_id' not in body or 'object_id' not in body or 'event_time' not in body:
        logger.error('Error processing new event from webhook due to missing parameters in the request body.')
        raise HTTPException(status_code=400, detail='Missing required request parameters')

    subscription_id = body['subscription_id']

    if int(subscription_id) != int(settings.STRAVA_SUBSCRIPTION_ID):
        logger.error('Error processing new event from webhook because the "subscription_id" '
                     'is different than expected. Provided subscription_id={}'.format(subscription_id))
        raise HTTPException(status_code=400, detail='Invalid subscription id')

    strava_notification: schemas.StravaNotification = schemas.StravaNotification(
        type=schemas.StravaNotificationType[body['object_type']],
        object_id=body['object_id'],
        action=schemas.StravaNotificationAction[body['aspect_type']],
        updates=body['updates'] if 'updates' in body else {},
        owner_id=int(body['owner_id']),
        event_time=datetime.fromtimestamp((int(body['event_time'])), timezone.utc)
    )

    logger.info('Received a new strava activity: {}'.format(strava_notification.dict()))
