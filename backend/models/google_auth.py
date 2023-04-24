from typing import TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

from backend.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class GoogleAuth(Base):
    id = Column(String(12), primary_key=True, index=True)
    token = Column(String, nullable=False)
    token_uri = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    expiry = Column(DateTime, nullable=False)
    refresh_token = Column(String, nullable=False)
    scopes = Column(ARRAY(String), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="google_auth")
