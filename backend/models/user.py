import enum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from .strava_credentials import StravaCredentials  # noqa: F401
    from .google_calendar_credentials import GoogleCalendarCredentials  # noqa: F401
    from .calendar_template import CalendarTemplate  # noqa: F401
    from .calendar_event import CalendarEvent  # noqa: F401


class UserStatus(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class AuthProvider(str, enum.Enum):
    GOOGLE = 'GOOGLE'


class UserBase(SQLModel):
    first_name: str = Field(index=True, nullable=False)
    last_name: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False, unique=True)
    auth_provider: AuthProvider = Field(nullable=False)
    auth_provider_id: str = Field(nullable=False)
    status: UserStatus = Field(nullable=False)
    is_superuser: bool = Field(nullable=False, default=False)

    strava_credentials: "StravaCredentials" = Relationship(back_populates="user")
    calendar_credentials: "GoogleCalendarCredentials" = Relationship(back_populates="user")
    calendar_templates: List["CalendarTemplate"] = Relationship(back_populates="user")
    calendar_events: List["CalendarEvent"] = Relationship(back_populates="user")


class User(UserBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: str
