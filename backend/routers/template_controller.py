from typing import Union

from backend.models import user_auth

from strava_calendar_summary_data_access_layer import User, UserController, CalendarPreferences
from strava_calendar_summary_utils import template_builder

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging
from pydantic import BaseModel

router = APIRouter(prefix='/summary/template')


class Template(BaseModel):
    summary_type: str
    enabled: Union[bool, None] = True
    title_template: Union[str, None] = None
    description_template: Union[str, None] = None


@router.post('/update')
async def update_template(template: Template, auth: user_auth.UserAuth = Depends(user_auth.get_signed_in_user_auth)):
    """
    Update the summary template for a calendar event
    :param template: information on what is being updated in the template
    :param auth: the signed-in user whose template is going to update
    :return: status code
    """
    await verify_summary_type(template.summary_type)

    invalid_keys: list = verify_templates(template.title_template,
                                          template.description_template,
                                          template.summary_type != 'per_activity')

    if len(invalid_keys) > 0:
        return JSONResponse(status_code=400, content={
            'error': 'Invalid keys found in the template',
            'invalid_keys': invalid_keys
        })

    user: User = UserController().get_by_id(auth.user_id)
    calendar_preferences: CalendarPreferences = user.calendar_preferences

    summary_type = template.summary_type
    enabled = template.enabled
    title_template = template.title_template
    description_template = template.description_template

    if summary_type == 'per_activity':
        calendar_preferences.per_run_summary_enabled = enabled
        if title_template is not None:
            calendar_preferences.per_run_title_template = title_template
        if description_template is not None:
            calendar_preferences.per_run_description_template = description_template
    elif summary_type == 'daily':
        calendar_preferences.daily_run_summary_enabled = enabled
        if title_template is not None:
            calendar_preferences.daily_run_title_template = title_template
        if description_template is not None:
            calendar_preferences.daily_run_description_template = description_template
    else:
        calendar_preferences.weekly_run_summary_enabled = enabled
        if title_template is not None:
            calendar_preferences.weekly_run_title_template = title_template
        if description_template is not None:
            calendar_preferences.weekly_run_description_template = description_template

    UserController().update(user.user_id, user)
    return 'Updated {} summary template'.format(summary_type)


def verify_templates(title_template: str, description_template: str, is_summary_template: bool) -> list:
    title_template_invalid_keys = []
    description_template_invalid_keys = []

    if title_template is not None:
        title_template_invalid_keys = template_builder.verify_template(title_template, is_summary_template)

    if description_template is not None:
        description_template_invalid_keys = template_builder.verify_template(description_template, is_summary_template)

    return list(set(title_template_invalid_keys + description_template_invalid_keys))


async def verify_summary_type(summary_type):
    if summary_type not in ['per_activity', 'daily', 'weekly']:
        logging.error('Summary: {} is not a valid summary type.'.format(summary_type))
        raise HTTPException(status_code=400, detail='Invalid summary type.')
