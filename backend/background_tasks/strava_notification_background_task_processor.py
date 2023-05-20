import time
from multiprocessing import Lock
from typing import Set

from backend.background_tasks.workers import StravaNotificationBackgroundTaskWorker
from backend.core import logger
from backend.models import StravaNotification

'''
Although Python lists are technically thread safe, the items within the list are not so I'm using a lock to ensure
that only one thread can access the list at a time.
'''
lock: Lock = Lock()
workers: Set[int] = set()  # Use set here since lookup is O(1) vs O(n) for lists


class StravaNotificationBackgroundTaskProcessor:
    def _acquite_lock(self, id: int) -> None:
        while True:
            with lock:
                if id not in workers:
                    workers.add(id)
                    break
                else:
                    logger.debug(f"Worker for user {id} is busy. Sleeping for 5 seconds.")
            time.sleep(5)

    def _release_lock(self, id: int) -> None:
        with lock:
            logger.debug(f"Releasing lock for user {id}")
            workers.remove(id)

    def process(self, notification: StravaNotification) -> None:
        """
        Process a Strava notification, only one notification per user can be processed at a time. If a notification
        is already being processed for a user, this method will block until the lock is released. This is to prevent
        multiple processing threads from trying to create the same calendar summary event for one user.
        """
        self._acquite_lock(notification.owner_id)
        try:
            logger.info("Processing activity for user: " + str(notification.owner_id))
            StravaNotificationBackgroundTaskWorker(notification).process()
            logger.info("Done processing")
        finally:
            self._release_lock(notification.owner_id)


strava_notification_background_task_processor: StravaNotificationBackgroundTaskProcessor = \
    StravaNotificationBackgroundTaskProcessor()
