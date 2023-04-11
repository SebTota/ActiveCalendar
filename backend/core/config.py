import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv('PROJECT_NAME')
    API_V1_STR: str = '/api/v1'
    API_HOST: str = f'http://localhost{API_V1_STR}'
    GOOGLE_AUTH_CALLBACK_URL: str = f'{API_HOST}/google_auth/callback'
    STRAVA_AUTH_CALLBACK_URL: str = f'{API_HOST}/strava_auth/callback'

    SECRET_KEY: str = os.getenv('API_CREDENTIALS_GENERATOR_SECRET_KEY')
    REFRESH_TOKEN_SECRET_KEY: str = os.getenv('API_CREDENTIALS_REFRESH_TOKEN_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (60 * 24 * 14)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = (60 * 24 * 90)

    DATABASE_USER: str = os.getenv('POSTGRES_USER')
    DATABASE_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    DATABASE_SERVER: str = os.getenv('POSTGRES_SERVER')
    DATABASE_DB: str = os.getenv('POSTGRES_DB')
    DATABASE_URL: str = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_SERVER}/{DATABASE_DB}'

    EMAIL_ACCOUNT_VERIFICATION_SECRET_KEY: str = os.getenv('ACCOUNT_VERIFICATION_SECRET_KEY')
    EMAIL_ACCOUNT_VERIFICATION_SALT: str = os.getenv('ACCOUNT_VERIFICATION_SALT')
    EMAIL_TEMPLATES_DIR: str = './backend/email_templates'
    EMAILS_FROM_NAME: str = PROJECT_NAME
    EMAILS_FROM_EMAIL: str = os.getenv('EMAILS_FROM_EMAIL')

    SMTP_HOST: str = os.getenv('SMTP_HOST')
    SMTP_PORT: int = os.getenv('SMTP_PORT')
    SMTP_USER: str = os.getenv('SMTP_USER')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD')

    STRAVA_WEBHOOK_VERIFICATION_TOKEN: str = os.getenv('STRAVA_WEBHOOK_VERIFICATION_TOKEN')
    STRAVA_SUBSCRIPTION_ID: str = os.getenv('STRAVA_SUBSCRIPTION_ID')
    STRAVA_CLIENT_ID: str = os.getenv('STRAVA_CLIENT_ID')
    STRAVA_CLIENT_SECRET: str = os.getenv('STRAVA_CLIENT_SECRET')


settings = Settings()
