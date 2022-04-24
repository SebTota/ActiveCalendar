from fastapi import APIRouter, Request, HTTPException
from strava_calendar_summary_web_service.config import STRAVA_WEBHOOK

router = APIRouter()


@router.get('/webhook')
def get_webhook(request: Request):
    params = request.query_params
    if 'hub.mode' not in params or 'hub.verify_token' not in params or 'hub.challenge' not in params:
        raise HTTPException(status_code=400, detail='Missing request parameters')

    hub_mode = params['hub.mode']
    hub_verification_token = params['hub.verify_token']
    hub_challenge = params['hub.challenge']

    if hub_mode == 'subscribe' and hub_verification_token == STRAVA_WEBHOOK['VERIFY_TOKEN']:
        print('Webhook verified')
        return {'hub.challenge': hub_challenge}
    else:
        raise HTTPException(status_code=403, detail='Webhook could not be verified')


@router.post('/webhook')
def post_webhook(request: Request):
    body = request.json()

    if 'subscription_id' not in body or 'object_type' not in body or 'aspect_type' not in body \
        or 'owner_id' not in body or 'object_id' not in body:
        raise HTTPException(status_code=400, detail='Missing request parameters')

    subscription_id = body['subscription_id']

    if int(subscription_id) != int(STRAVA_WEBHOOK['SUBSCRIPTION_ID']):
        raise HTTPException(status_code=400, detail='Invalid subscription id')

    object_type = body['object_type']
    aspect_type = body['aspect_type']  ## Create, update, delete
    user_id = body['owner_id']
    activity_id = body['object_id']

    # Ignore none 'activity' events
    if object_type != 'activity':
        return {}

    print('Received a new {} activity: {} event for user: {}'.format(
        aspect_type, activity_id, user_id
    ))
