import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = os.getenv('API_CREDENTIALS_GENERATOR_SECRET_KEY')
    REFRESH_TOKEN_SECRET_KEY: str = os.getenv('API_CREDENTIALS_REFRESH_TOKEN_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (60 * 24 * 14)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = (60 * 24 * 90)

    DATABASE_PASSWORD: str = os.getenv('DATABASE_PASSWORD')
    DATABASE_URL: str = f'postgresql://postgres:{DATABASE_PASSWORD}@database-1.cxabyrsbraij.eu-central-1.rds.amazonaws.com/active_calendar'

    SMTP_USERNAME: str = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD')
    SMTP_MAIL_FROM: str = os.getenv('SMTP_MAIL_FROM')


settings = Settings()