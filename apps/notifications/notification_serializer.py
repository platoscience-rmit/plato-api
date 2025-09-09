from rest_framework import serializers
from apps.notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'title',
            'type',
            'description',
            'is_readed',
            'created_at',
            'assessment_time'
        ]