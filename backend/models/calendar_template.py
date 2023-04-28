import enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class CalendarTemplateType(str, enum.Enum):
    ACTIVITY_SUMMARY = 'ACTIVITY_SUMMARY'
    DAILY_SUMMARY = 'DAILY_SUMMARY'
    WEEKLY_SUMMARY = 'WEEKLY_SUMMARY'


class CalendarTemplateStatus(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    DISABLED = 'DISABLED'


class CalendarTemplate(Base):
    id: Mapped[str] = Column(String(12), primary_key=True, index=True)
    status: Mapped[CalendarTemplateStatus] = Column(Enum(CalendarTemplateStatus), index=True, nullable=False)
    type: Mapped[CalendarTemplateType] = Column(Enum(CalendarTemplateType), index=True, nullable=False)
    title_template: Mapped[str] = Column(String, nullable=False)
    body_template: Mapped[str] = Column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="calendar_templates")
