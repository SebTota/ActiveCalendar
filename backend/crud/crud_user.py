from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from backend.core.security import get_password_hash, verify_password
from backend.crud.base import CRUDBase
from backend.models.user import User, UserStatus
from backend.schemas.user import UserCreate, UserUpdate
from backend.utils import get_random_alphanumeric_string


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session,
                    obj_in: UserCreate,
                    status: UserStatus = UserStatus.ACTIVE.value,
                    is_superuser: bool = False) -> User:
        db_obj = User(
            id=get_random_alphanumeric_string(12),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            auth_provider=obj_in.auth_provider,
            auth_provider_id=obj_in.auth_provider_id,
            status=status,
            is_superuser=is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_pending_email_verification(self, user: User) -> bool:
        return user.status == UserStatus.PENDING_EMAIL_VERIFICATION

    def is_active(self, user: User) -> bool:
        return user.status == UserStatus.ACTIVE

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
