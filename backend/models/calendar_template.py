import enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class CalendarTemplateType(str, enum.Enum):
    ACTIVITY_SUMMARY = 'ACTIVITY_SUMMARY'
    DAILY_SUMMARY = 'DAILY_SUMMARY'
    WEEKLY_SUMMARY = 'WEEKLY_SUMMARY'


class CalendarTemplateStatus(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    DISABLED = 'DISABLED'


class CalendarTemplateBase(SQLModel):
    status: CalendarTemplateStatus = Field(index=True, nullable=False)
    type: CalendarTemplateType = Field(index=True, nullable=False)
    title_template: str = Field(nullable=False)
    body_template: str = Field(nullable=False)
    user_id: str = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="calendar_templates")


class CalendarTemplate(CalendarTemplateBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)


class CalendarTemplateCreate(CalendarTemplateBase):
    pass


class CalendarTemplateRead(CalendarTemplateBase):
    id: str


class CalendarTemplateUpdate(SQLModel):
    status: Optional[CalendarTemplateStatus] = None
    type: Optional[CalendarTemplateType] = None
    title_template: Optional[str] = None
    body_template: Optional[str] = None
