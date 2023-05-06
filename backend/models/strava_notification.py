import datetime
from enum import Enum

from pydantic import BaseModel


class StravaNotificationType(str, Enum):
    activity = 'activity'
    athlete = 'athlete'


class StravaNotificationAction(str, Enum):
    create = 'create'
    update = 'update'
    delete = 'delete'


class StravaNotification(BaseModel):
    type: StravaNotificationType
    object_id: int
    action: StravaNotificationAction
    updates: dict
    owner_id: int
    event_time: datetime.datetime
