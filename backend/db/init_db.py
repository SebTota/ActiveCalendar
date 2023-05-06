from sqlmodel import SQLModel

from backend.core import logger
from backend.db.session import engine
from backend import models  # DO NOT DELETE THIS!


def init_db() -> None:
    logger.info("Creating db connection and inti engine...")
    SQLModel.metadata.create_all(engine)
    logger.info("Created db connection...")
