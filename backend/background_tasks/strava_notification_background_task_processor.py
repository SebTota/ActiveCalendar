from backend import schemas
from backend.background_tasks.workers import StravaNotificationBackgroundTaskWorker


class StravaNotificationBackgroundTaskProcessor:

    def process(self, notification: schemas.StravaNotification):
        worker: StravaNotificationBackgroundTaskWorker = StravaNotificationBackgroundTaskWorker(notification)
        worker.process()


strava_notification_background_task_processor: StravaNotificationBackgroundTaskProcessor = \
    StravaNotificationBackgroundTaskProcessor()
