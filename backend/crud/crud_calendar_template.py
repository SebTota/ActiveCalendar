from typing import Optional

from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models import CalendarTemplate, User
from backend.schemas import CalendarTemplateCreate, CalendarTemplateUpdate, CalendarTemplateType
from backend.utils.base_utils import get_random_alphanumeric_string


class CRUDCalendarTemplate(CRUDBase[CalendarTemplate, CalendarTemplateCreate, CalendarTemplateUpdate]):

    def get_template_by_type(self, db: Session,
                             user_id: str, template_type: CalendarTemplateType) -> Optional[CalendarTemplate]:
        return db.query(CalendarTemplate).filter(User.id == user_id, CalendarTemplate.type == template_type).first()

    def create_and_add_to_user(self, db: Session, user_id: str, obj: CalendarTemplateUpdate):
        db_obj: CalendarTemplate = CalendarTemplate(id=get_random_alphanumeric_string(12),
                                                    status=obj.status,
                                                    type=obj.type,
                                                    title_template=obj.title_template,
                                                    body_template=obj.body_template,
                                                    user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


calendar_template = CRUDCalendarTemplate(CalendarTemplate)
