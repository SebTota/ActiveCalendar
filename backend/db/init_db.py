from sqlalchemy.orm import Session

from backend.core import logger
from backend.db.base_class import Base
from backend.db.session import engine


def init_db(db: Session) -> None:
    logger.info("Creating db connection...")
    Base.metadata.create_all(bind=engine)
    logger.debug("Created db connection...")
