from typing import Optional

from sqlmodel import Session

from backend.models.user import User, UserStatus, UserCreate
from backend.utils import get_random_alphanumeric_string


def get(db: Session, obj_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == obj_id).first()


def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, obj: UserCreate) -> User:
    db_obj: User = User.from_orm(obj)
    db_obj.id = get_random_alphanumeric_string(12)
    db_obj.is_superuser = False
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, obj: User) -> User:
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def is_active(user: User) -> bool:
    return user.status == UserStatus.ACTIVE


def is_superuser(user: User) -> bool:
    return user.is_superuser
