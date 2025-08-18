from apps.common.base_repository import BaseRepository
from apps.notifications.models import Notification

class NotificationRepository(BaseRepository):
    def __init__(self):
        super().__init__(Notification)