from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class CalendarEvent(Base):
    id: Mapped[str] = Column(String(20), primary_key=True, index=True)
    start_date: Mapped[datetime] = Column(DateTime, nullable=False, index=True)
    end_date: Mapped[datetime] = Column(DateTime, nullable=False, index=True)
    strava_event_id: Mapped[int] = Column(BigInteger, nullable=True, index=True, unique=True)
    calendar_event_id: Mapped[str] = Column(String, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="calendar_events")
