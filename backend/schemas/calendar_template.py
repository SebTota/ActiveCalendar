from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class CalendarTemplateStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    DISABLED = 'DISABLED'


class CalendarTemplateType(str, Enum):
    ACTIVITY_SUMMARY = 'ACTIVITY_SUMMARY'
    DAILY_SUMMARY = 'DAILY_SUMMARY'
    WEEKLY_SUMMARY = 'WEEKLY_SUMMARY'


# Shared properties
class CalendarTemplateBase(BaseModel):
    status: Optional[CalendarTemplateStatus]
    type: Optional[CalendarTemplateType]
    title_template: Optional[str]
    body_template: Optional[str]


class CalendarTemplateCreate(BaseModel):
    status: CalendarTemplateStatus
    type: CalendarTemplateType
    title_template: str
    body_template: str


class CalendarTemplateUpdate(CalendarTemplateBase):
    pass


class CalendarTemplateInDBBase(CalendarTemplateBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True


# Additional properties to return via API
class CalendarTemplate(CalendarTemplateInDBBase):
    pass


# Additional properties stored in DB
class CalendarTemplateInDB(CalendarTemplateInDBBase):
    pass
