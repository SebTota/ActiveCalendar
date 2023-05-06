from sqlmodel import create_engine

from backend.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
