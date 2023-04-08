import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Active Calendar'
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = os.getenv('API_CREDENTIALS_GENERATOR_SECRET_KEY')
    REFRESH_TOKEN_SECRET_KEY: str = os.getenv('API_CREDENTIALS_REFRESH_TOKEN_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (60 * 24 * 14)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = (60 * 24 * 90)

    DATABASE_PASSWORD: str = os.getenv('DATABASE_PASSWORD')
    DATABASE_URL: str = f'postgresql://postgres:{DATABASE_PASSWORD}@database-1.cxabyrsbraij.eu-central-1.rds.amazonaws.com/active_calendar'

    EMAIL_ACCOUNT_VERIFICATION_SECRET_KEY: str = os.getenv('ACCOUNT_VERIFICATION_SECRET_KEY')
    EMAIL_ACCOUNT_VERIFICATION_SALT: str = os.getenv('ACCOUNT_VERIFICATION_SALT')
    EMAIL_TEMPLATES_DIR: str = './backend/email_templates'
    EMAILS_FROM_NAME: str = 'Active Calendar'
    EMAILS_FROM_EMAIL: str = 'account_services@active.sebtota.com'

    SMTP_HOST: str = os.getenv('SMTP_SERVER')
    SMTP_PORT: int = 587
    SMTP_USER: str = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD')


settings = Settings()
