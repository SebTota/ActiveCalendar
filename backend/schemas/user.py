from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


# User status enum
class UserStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    PENDING_EMAIL_VERIFICATION = 'PENDING_EMAIL_VERIFICATION'
    INACTIVE = 'INACTIVE'


# Shared properties
class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[UserStatus] = None
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(BaseModel):
    password: Optional[str] = None


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
