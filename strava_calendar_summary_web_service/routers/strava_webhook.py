from fastapi import APIRouter, Request, HTTPException
from strava_calendar_summary_web_service.config import STRAVA_WEBHOOK

router = APIRouter()


@router.get('/webhook')
def get_webhook(request: Request):
    hub_mode = request.query_params['hub.mode']
    hub_verification_token = request.query_params['hub.verify_token']
    hub_challenge = request.query_params['hub.challenge']

    if hub_mode == 'subscribe' and hub_verification_token == STRAVA_WEBHOOK['VERIFY_TOKEN']:
        print('Webhook verified')
        return {'hub.challenge': hub_challenge}
    else:
        raise HTTPException(status_code=403, detail='Webhook could not be verified')


@router.post('/webhook')
def post_webhook(request: Request):
    body = request.json()
    subscription_id = body['subscription_id']

    if int(subscription_id) != int(STRAVA_WEBHOOK['SUBSCRIPTION_ID']):
        raise HTTPException(status_code=400, detail='invalid subscription id')

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
