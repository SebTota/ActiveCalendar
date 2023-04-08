import logging
from pathlib import Path
from typing import Dict, Any

import emails
from emails.template import JinjaTemplate

from backend.core.config import settings


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {}
) -> None:
    message = emails.html(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {
        "host": settings.SMTP_HOST,
        "port": settings.SMTP_PORT,
        "tls": True,
        "user": settings.SMTP_USER,
        "password": settings.SMTP_PASSWORD
    }
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    print(f"send email result: {response}")


def send_new_account_email(email_to: str, first_name: str, verification_link: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Account Verification"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "first_name": first_name,
            "verification_link": verification_link,
        },
    )
