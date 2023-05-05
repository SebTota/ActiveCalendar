import enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Column, String, Enum
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field, Relationship

from backend.db.base_class import Base

if TYPE_CHECKING:
    from .strava_credentials import StravaCredentials  # noqa: F401
    from .google_calendar_credentials import GoogleCalendarCredentials  # noqa: F401
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
    google_calendar_auth = relationship("GoogleCalendarAuth", back_populates="user", cascade="all, delete-orphan")
    calendar_templates = relationship("CalendarTemplate", back_populates="user", cascade="all, delete-orphan")
    calendar_events = relationship("CalendarEvent", back_populates="user", cascade="all, delete-orphan")




class UserBase(SQLModel):
    first_name: str = Field(index=True, nullable=False)
    last_name: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)
    auth_provider: AuthProvider = Field(nullable=False)
    auth_provider_id: str = Field(nullable=False)
    status: UserStatus = Field(nullable=False)
    is_superuser: bool = Field(nullable=False, default=False)

    strava_credentials: StravaCredentials = Relationship(back_populates="user")
    calendar_credentials: GoogleCalendarCredentials = Relationship(back_populates="user")
    calendar_templates: List[CalendarTemplate] = Relationship(back_populates="user")
    calendar_events: List[CalendarEvent] = Relationship(back_populates="user")


class User(UserBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: str

