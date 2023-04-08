import enum

from sqlalchemy import Boolean, Column, String, Enum

from backend.db.base_class import Base


class UserStatus(str, enum.Enum):
    ACTIVE = 'ACTIVE'
    PENDING_EMAIL_VERIFICATION = 'PENDING_EMAIL_VERIFICATION'
    INACTIVE = 'INACTIVE'


class User(Base):
    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    status = Column(Enum(UserStatus), nullable=False)
    is_superuser = Column(Boolean(), default=False, nullable=False)
