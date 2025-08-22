from django.shortcuts import render
from rest_framework.views import APIView
from apps.notifications.notification_service import NotificationService
from rest_framework.response import Response
from rest_framework import status
from apps.notifications.notification_serializer import NotificationSerializer
from apps.notifications.notification_schema import notifications_schema, read_notification_schema

@notifications_schema
class NotificationView(APIView):
    def __init__(self):
        self.service = NotificationService()
        
    def get(self, request):
        user = request.user
        
        try:
            data = self.service.filter(user_id=user.id)
            return Response(NotificationSerializer(data, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
@read_notification_schema
class ReadNotificationView(APIView):
    def __init__(self):
        self.service = NotificationService()
        
    def post(self, request):
        user = request.user
        notification_id = request.data.get('notification_id')
        try:
            notification = self.service.read_notification(user, notification_id)
            if (notification):
                return Response(NotificationSerializer(notification).data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No notification found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            