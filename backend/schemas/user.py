from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


# User status enum
class UserStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    PENDING_EMAIL_VERIFICATION = 'PENDING_EMAIL_VERIFICATION'
    INACTIVE = 'INACTIVE'


class AuthProvider(str, Enum):
    GOOGLE = 'GOOGLE'


# Shared properties
class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    auth_provider: Optional[AuthProvider] = None
    auth_provider_id: Optional[str] = None
    status: Optional[UserStatus] = None
    is_superuser: bool = False


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    auth_provider: AuthProvider
    auth_provider_id: str


# Properties to receive via API on update
class UserUpdate(BaseModel):
    pass

class UserInDBBase(UserBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
