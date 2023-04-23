from typing import TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class StravaCredentials(Base):
    id = Column(Integer, primary_key=True, index=True)  # Also the athlete's Strava id
    access_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    refresh_token = Column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="strava_credentials")
