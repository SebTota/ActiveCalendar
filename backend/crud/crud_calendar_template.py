from typing import Optional

from sqlmodel import Session

from backend.models import CalendarTemplate, User
from backend.models.calendar_template import CalendarTemplateStatus, CalendarTemplateType, CalendarTemplateCreate
from backend.utils.base_utils import get_random_alphanumeric_string


def get_template_by_type(db: Session, user_id: str, template_type: CalendarTemplateType) -> Optional[CalendarTemplate]:
    return db.query(CalendarTemplate).filter(User.id == user_id, CalendarTemplate.type == template_type).first()


def get_activity_template(db: Session, user_id: str) -> Optional[CalendarTemplate]:
    return db.query(CalendarTemplate).filter(User.id == user_id,
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
    templates = db.query(CalendarTemplate).filter(User.id == user_id,
                                                  CalendarTemplate.status == CalendarTemplateStatus.ACTIVE).all()
    for template in templates:
        temps[template.type] = template
    return temps


def create_and_add_to_user(self, db: Session, obj: CalendarTemplateCreate):
    db_obj: CalendarTemplate = CalendarTemplate.from_orm(obj)
    db_obj.id = get_random_alphanumeric_string(12)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
