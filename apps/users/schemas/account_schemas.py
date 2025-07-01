from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers.user_serializer import UserSerializer

account_create_schema = extend_schema(
    summary="Create new account",
    description="Create a new user account with email and password.",
    request=UserSerializer,
    responses={
        201: OpenApiResponse(
            description="Account created successfully",
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "status": "success",
                        "message": "Account created successfully",
                        "user": {
                            "email": "user@example.com",
                            "user_id": 1
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Validation error or account creation failed"),
    },
    tags=["Accounts"]
)