from fastapi import APIRouter, Request, HTTPException
import os

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
        or 'owner_id' not in body or 'object_id' not in body:
        raise HTTPException(status_code=400, detail='Missing required request parameters')

    subscription_id = body['subscription_id']

    if int(subscription_id) != int(os.getenv('STRAVA_SUBSCRIPTION_ID')):
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
