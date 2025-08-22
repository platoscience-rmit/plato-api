from apps.common.base_service import BaseService
from apps.notifications.notification_repository import NotificationRepository

class NotificationService(BaseService):
    def __init__(self):
        super().__init__(NotificationRepository())
        
    def read_notification(self, user, notification_id):
        notification = self.filter(user_id=user.id, id=notification_id).first()
        
        if (notification):
            self.update(notification.id, is_readed=True)
            notification.refresh_from_db() 
            return notification
        
        return None