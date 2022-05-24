from backend.models import user_auth

from strava_calendar_summary_data_access_layer import User, UserController, StravaCredentials, CalendarPreferences
from strava_calendar_summary_utils import template_builder

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging
import json

router = APIRouter(prefix='/summary/template')


@router.get('/verify')
async def verify_summary_template(summary_type: str, title_template: str, summary_template: str):
    await verify_summary_type(summary_type)
    invalid_keys: list = verify_templates(title_template, summary_template)

    if len(invalid_keys) > 0:
        return JSONResponse(status_code=400, content={
            'error': 'Invalid keys found in the template',
            'invalid_keys': invalid_keys
        })
    else:
        return ''


@router.post('/update')
async def update_summary_template(summary_type: str, enabled: bool, title_template: str = None, summary_template: str = None, auth: user_auth.UserAuth = Depends(user_auth.get_signed_in_user_auth)):
    """
    Update the summary template for a calendar event
    :param enabled:
    :param summary_template:
    :param title_template:
    :param summary_type: per_run, daily, or weekly calendar summary template type
    :param request: the HTTP request whose body contains what is going to be updated
        {
            'enabled': str // 'true' to enable or any other string to disable
            'title_template': str // Optional
            'summary_template': str // Optional
        }
    :param auth: the signed-in user whose template is going to update
    :return: status code
    """
    await verify_summary_type(summary_type)

    invalid_keys: list = verify_templates(title_template, summary_template)

    if len(invalid_keys) > 0:
        return JSONResponse(status_code=400, content={
            'error': 'Invalid keys found in the template',
            'invalid_keys': invalid_keys
        })

    user: User = UserController().get_by_id(auth.user_id)
    calendar_preferences: CalendarPreferences = user.calendar_preferences

    if summary_type == 'per_activity':
        calendar_preferences.per_run_summary_enabled = enabled
        if title_template is not None:
            calendar_preferences.per_run_title_template = title_template
        if summary_template is not None:
            calendar_preferences.per_run_summary_template = summary_template
    elif summary_type == 'daily':
        calendar_preferences.daily_run_summary_enabled = enabled
        if title_template is not None:
            calendar_preferences.daily_run_title_template = title_template
        if summary_template is not None:
            calendar_preferences.daily_run_summary_template = summary_template
    else:
        calendar_preferences.weekly_run_summary_enabled = enabled
        if title_template is not None:
            calendar_preferences.weekly_run_title_template = title_template
        if summary_template is not None:
            calendar_preferences.weekly_run_summary_template = summary_template

    UserController().update(user.user_id, user)
    return 'Updated {} summary template'.format(summary_type)


def verify_templates(title_template: str, summary_template: str) -> list:
    title_template_invalid_keys = []
    summary_template_invalid_keys = []

    if title_template is not None:
        title_template_invalid_keys = template_builder.verify_template(title_template)

    if summary_template is not None:
        summary_template_invalid_keys = template_builder.verify_template(summary_template)

    return list(set(title_template_invalid_keys + summary_template_invalid_keys))


async def verify_summary_type(summary_type):
    if summary_type not in ['per_activity', 'daily', 'weekly']:
        logging.error('Summary: {} is not a valid summary type.'.format(summary_type))
        raise HTTPException(status_code=400, detail='Invalid summary type.')
