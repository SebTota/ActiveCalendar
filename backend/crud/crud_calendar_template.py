from fastapi import HTTPException
from typing import Optional

from sqlmodel import Session

from backend.models import CalendarTemplateStatus, CalendarTemplateType, CalendarTemplateCreate, \
    CalendarTemplateUpdate, CalendarTemplate
from backend.utils.base_utils import get_random_alphanumeric_string

DEFAULT_EVENT_TITLE_TEMPLATE: str = '{distance_miles} {type}'
DEFAULT_EVENT_DESCRIPTION_TEMPLATE: str = 'Name: {name}\n' \
                                          'Distance: {distance_miles}\n' \
                                          'Duration: {duration}\n' \
                                          'Pace: {pace_min_per_mile}'
DEFAULT_SUMMARY_TITLE_TEMPLATE: str = 'Total Distance: {distance_miles}'
DEFAULT_SUMMARY_DESCRIPTION_TEMPLATE: str = 'Total Distance: {distance_miles}\n' \
                                            'Total Duration: {duration}\n' \
                                            'Total Elevation Gain: {elevation_gain_feet}\n' \
                                            'Average Pace: {avg_pace_min_per_mile}'


def get(db: Session, obj_id: str) -> Optional[CalendarTemplate]:
    return db.query(CalendarTemplate).filter(CalendarTemplate.id == obj_id).first()


def update(db: Session, obj_id: str, obj: CalendarTemplateUpdate) -> CalendarTemplate:
    db_obj = db.get(CalendarTemplate, obj_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="DB obj not found")
    obj_data = obj.dict(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(db_obj, key, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_template_by_type(db: Session, user_id: str, template_type: CalendarTemplateType) -> Optional[CalendarTemplate]:
    return db.query(CalendarTemplate).filter(CalendarTemplate.user_id == user_id,
                                             CalendarTemplate.type == template_type).first()


def get_activity_template(db: Session, user_id: str) -> Optional[CalendarTemplate]:
    return db.query(CalendarTemplate).filter(CalendarTemplate.user_id == user_id,
                                             CalendarTemplate.status == CalendarTemplateStatus.ACTIVE,
                                             CalendarTemplate.type == CalendarTemplateType.ACTIVITY_SUMMARY).first()


def get_all_active_templates(db: Session, user_id: str) -> dict:
    """
    Get a dictionary that contains all the active templates for a given user.

    {
        models.CalendarTemplateType: CalendarTemplate
    }
    """
    temps: {} = {}
    templates = db.query(CalendarTemplate).filter(CalendarTemplate.user_id == user_id,
                                                  CalendarTemplate.status == CalendarTemplateStatus.ACTIVE).all()
    for template in templates:
        temps[template.type] = template
    return temps


def create_and_add_to_user(db: Session, obj: CalendarTemplateCreate) -> CalendarTemplate:
    db_obj: CalendarTemplate = CalendarTemplate.from_orm(obj)
    db_obj.id = get_random_alphanumeric_string(12)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_multiple_and_add_to_user(db: Session, objs: [CalendarTemplateCreate]) -> None:
    for obj in objs:
        db_obj: CalendarTemplate = CalendarTemplate.from_orm(obj)
        db_obj.id = get_random_alphanumeric_string(12)
        db.add(db_obj)
    db.commit()


def create_default_templates_for_new_user(db: Session, user_id: str) -> [CalendarTemplate]:
    activity_summary_template = CalendarTemplateCreate(status=CalendarTemplateStatus.DISABLED,
                                                       type=CalendarTemplateType.ACTIVITY_SUMMARY,
                                                       title_template=DEFAULT_EVENT_TITLE_TEMPLATE,
                                                       body_template=DEFAULT_EVENT_DESCRIPTION_TEMPLATE,
                                                       user_id=user_id)

    daily_summary_template = CalendarTemplateCreate(status=CalendarTemplateStatus.DISABLED,
                                                    type=CalendarTemplateType.DAILY_SUMMARY,
                                                    title_template=DEFAULT_SUMMARY_TITLE_TEMPLATE,
                                                    body_template=DEFAULT_SUMMARY_DESCRIPTION_TEMPLATE,
                                                    user_id=user_id)

    weekly_summary_template = CalendarTemplateCreate(status=CalendarTemplateStatus.DISABLED,
                                                     type=CalendarTemplateType.WEEKLY_SUMMARY,
                                                     title_template=DEFAULT_SUMMARY_TITLE_TEMPLATE,
                                                     body_template=DEFAULT_SUMMARY_DESCRIPTION_TEMPLATE,
                                                     user_id=user_id)

    templates = [activity_summary_template, daily_summary_template, weekly_summary_template]
    create_multiple_and_add_to_user(db, templates)
