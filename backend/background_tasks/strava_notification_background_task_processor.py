from backend import schemas
from backend.background_tasks.workers import StravaNotificationBackgroundTaskWorker
from backend.models import StravaNotification


class StravaNotificationBackgroundTaskProcessor:

    def process(self, notification: StravaNotification):
        worker: StravaNotificationBackgroundTaskWorker = StravaNotificationBackgroundTaskWorker(notification)
        worker.process()


strava_notification_background_task_processor: StravaNotificationBackgroundTaskProcessor = \
    StravaNotificationBackgroundTaskProcessor()
