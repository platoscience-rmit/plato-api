from apps.common.base_service import BaseService
from apps.notifications.notification_repository import NotificationRepository

class NotificationService(BaseService):
    def __init__(self):
        super().__init__(NotificationRepository())