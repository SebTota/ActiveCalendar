from datetime import datetime, timezone, timedelta
from backend.core import logger


def beginning_of_day_in_utc(date: datetime) -> datetime:
    d = date.replace(hour=0, minute=0, second=0, microsecond=0)
    return datetime.fromtimestamp(d.timestamp(), tz=timezone.utc)


def end_of_day_in_utc(date: datetime) -> datetime:
    d = date.replace(hour=23, minute=59, second=59, microsecond=0)
    return datetime.fromtimestamp(d.timestamp(), tz=timezone.utc)


def beginning_of_week_in_utc(date: datetime) -> datetime:
    """
    Get the date for the beginning of the week of the given date in UTC, assuming Monday is the FIRST day of the week.
    """
    d = date.replace(hour=0, minute=0, second=0, microsecond=0)
    d = d - timedelta(days=d.weekday())
    return datetime.fromtimestamp(d.timestamp(), tz=timezone.utc)


def end_of_week_in_utc(date: datetime) -> datetime:
    """
    Get the date for the end of the week of the given date in UTC, assuming Sunday is the LAST day of the week.
    """
    d = date.replace(hour=23, minute=59, second=59, microsecond=0)
    d = d - timedelta(days=d.weekday()) + timedelta(days=6)
    return datetime.fromtimestamp(d.timestamp(), tz=timezone.utc)
