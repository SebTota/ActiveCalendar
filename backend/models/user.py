import enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String, Enum
from sqlalchemy.orm import relationship

from backend.db.base_class import Base

if TYPE_CHECKING:
    from .strava_credentials import StravaCredentials  # noqa: F401
    from .google_auth import GoogleAuth  # noqa: F401
    from .calendar_template import CalendarTemplate  # noqa: F401
    from .calendar_event import CalendarEvent  # noqa: F401


class UserStatus(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    PENDING_EMAIL_VERIFICATION = 'PENDING_EMAIL_VERIFICATION'
    INACTIVE = 'INACTIVE'


class AuthProvider(str, enum.Enum):
    GOOGLE = 'GOOGLE'


class User(Base):
    id = Column(String(length=12), primary_key=True, index=True)
    first_name = Column(String(length=100), index=True, nullable=False)
    last_name = Column(String(length=100), index=True, nullable=False)
    email = Column(String(length=254), unique=True, index=True, nullable=False)
    auth_provider = Column(Enum(AuthProvider), nullable=False)
    auth_provider_id = Column(String(length=256), nullable=False)
    status = Column(Enum(UserStatus), nullable=False)
    is_superuser = Column(Boolean(), default=False, nullable=False)
    strava_credentials = relationship("StravaCredentials", back_populates="user", cascade="all, delete-orphan")
    google_auth = relationship("GoogleAuth", back_populates="user", cascade="all, delete-orphan")
    calendar_templates = relationship("CalendarTemplate", back_populates="user", cascade="all, delete-orphan")
    calendar_events = relationship("CalendarEvent", back_populates="user", cascade="all, delete-orphan")
