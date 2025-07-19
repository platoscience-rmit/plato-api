from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.assessments.serializers.question_serializer import (QuestionSerializer)

question_list_schema = extend_schema(
    summary="List Questions",
    description="Retrieve a list of questions for the authenticated user.",
    responses={
        200: OpenApiResponse(
            description="List of questions retrieved successfully",
            response=QuestionSerializer(many=True),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value=[
                        {
                            "id": 1,
                            "name": "Math Question",
                            "content": "What is 2 + 2?",
                            "description": "A basic math question.",
                            "category": "Math",
                            "options": [
                                {"id": 1, "content": "3", "is_correct": False},
                                {"id": 2, "content": "4", "is_correct": True},
                                {"id": 3, "content": "5", "is_correct": False}
                            ]
                        },
                        {
                            "id": 2,
                            "name": "Science Question",
                            "content": "What is the chemical symbol for water?",
                            "description": "A basic science question.",
                            "category": "Science",
                            "options": [
                                {"id": 4, "content": "H2O", "is_correct": True},
                                {"id": 5, "content": "CO2", "is_correct": False},
                                {"id": 6, "content": "O2", "is_correct": False}
                            ]
                        }
                    ]
                )
            ]
        )
    }
)
