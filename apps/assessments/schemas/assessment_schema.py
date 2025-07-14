from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.assessments.serializers.assessment_serializer import (
    AssessmentSerializer
)

assessment_list_schema = extend_schema(
    summary="List Assessments",
    description="Retrieve a list of assessments for the authenticated user.",
    responses={
        200: OpenApiResponse(
            description="List of assessments retrieved successfully",
            response=AssessmentSerializer(many=True),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value=[
                        {
                            "id": 1,
                            "title": "Math Assessment",
                            "description": "An assessment on basic math skills.",
                            "created_at": "2023-10-01T12:00:00Z",
                            "phq_score": 12,
                            "bdi_score": 25,
                            "plato_score": 3.0,
                            "protocol": {
                                "intensity": "Medium",
                                "duration": "20 mins",
                                "node_placement": "Left Arm",
                                "node_type": "Type B",
                                "node_size": "Medium"
                            },
                            "severity": 1,
                            "answers": [
                                {
                                    "id": 1,
                                    "question": "What is 2 + 2?",
                                    "answer": "4",
                                    "index": 0
                                },
                                {
                                    "id": 2,
                                    "question": "What is the capital of France?",
                                    "answer": "Paris",
                                    "index": 1
                                }
                            ]
                            
                        },
                        {
                            "id": 2,
                            "title": "Science Assessment",
                            "description": "An assessment on basic science concepts.",
                            "created_at": "2023-10-02T12:00:00Z",
                            "phq_score": 10,
                            "bdi_score": 20,
                            "plato_score": 2.5,
                            "protocol": {
                                "intensity": "Low",
                                "duration": "15 mins",
                                "node_placement": "Right Arm",
                                "node_type": "Type A",
                                "node_size": "Small"
                            },
                            "severity": 0,
                            "answers": [
                                {
                                    "id": 3,
                                    "question": "What is the chemical symbol for water?",
                                    "answer": "H2O",
                                    "index": 0
                                },
                                {
                                    "id": 4,
                                    "question": "What planet is known as the Red Planet?",
                                    "answer": "Mars",
                                    "index": 1
                                }
                            ]
                        }
                    ]
                )
            ]
        ),
        401: OpenApiResponse(description="Authentication required"),
        403: OpenApiResponse(description="Forbidden access")
    },
    tags=["Assessments"]
)
