from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.notifications.notification_serializer import NotificationSerializer

notifications_schema = extend_schema(
    summary="Get all notifications for the current user",
    description="Returns a list of notifications for the authenticated user.",
    responses={
        200: OpenApiResponse(
            response=NotificationSerializer(many=True),
            description="List of notifications",
            examples=[
                OpenApiExample(
                    "Success Response",
                    value=[
                        {
                            "id": 1,
                            "title": "Assessment Ended",
                            "description": "Your assessment period has ended.",
                            "is_readed": False,
                            "created_at": "2025-08-18T15:48:10Z"
                        }
                    ]
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad request",
            examples=[
                OpenApiExample(
                    "Error Response",
                    value={"error": "Some error message"}
                )
            ]
        ),
        401: OpenApiResponse(description="Authentication required"),
    },
    tags=["Notifications"]
)

read_notification_schema = extend_schema(
    summary="Mark a notification as read",
    description="Marks the specified notification as read for the authenticated user and returns the updated notification.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "notification_id": {
                    "type": "integer",
                    "example": 1
                }
            },
            "required": ["notification_id"]
        }
    },
    responses={
        200: OpenApiResponse(
            response=NotificationSerializer,
            description="Notification marked as read",
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "id": 1,
                        "title": "Assessment Ended",
                        "description": "Your assessment period has ended.",
                        "is_readed": True,
                        "created_at": "2025-08-18T15:48:10Z"
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad request",
            examples=[
                OpenApiExample(
                    "Error Response",
                    value={"error": "No notification found"}
                )
            ]
        ),
        401: OpenApiResponse(description="Authentication required"),
    },
    tags=["Notifications"]
)