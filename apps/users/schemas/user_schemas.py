from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.users.serializers.user_serializer import UserSerializer

user_create_schema = extend_schema(
    summary="Create new user",
    description="Create a new user user with email and password.",
    request=UserSerializer,
    responses={
        201: OpenApiResponse(
            description="User created successfully",
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "status": "success",
                        "message": "User created successfully",
                        "user": {
                            "email": "user@example.com",
                            "user_id": 1
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="Validation error or User creation failed"),
    },
    tags=["Accounts"]
)
