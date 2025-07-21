from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.assessments.serializers.assessment_serializer import (
    AssessmentSerializer,
    CreateAssessmentSerializer
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
                                    "answer": "null",
                                    "selected_option": {
                                        "id": 1,
                                        "label": "test option",
                                        "value": "testttt"
                                    },
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

create_assessment_schema = extend_schema(
    summary="Create Assessment",
    description="Create a new assessment with answers.",
    request=CreateAssessmentSerializer(),
    examples=[
        OpenApiExample(
            'Example Request',
            value={
                "answers": [
                    {
                        "question": 5,
                        "answer": "answer 1",
                        "selected_option": 4,
                        "index": 0
                    },
                    {
                        "question": 9,
                        "answer": "answer 2",
                        "selected_option": 15,
                        "index": 3
                    },
                    {
                        "question": 10,
                        "answer": "answer 3",
                        "selected_option": 18,
                        "index": 3
                    }
                ]
            },
            request_only=True,
        )
    ],
    responses={
        201: OpenApiResponse(
            description="Create a new assessment successfully",
            response=AssessmentSerializer(),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "status": "success",
                        "message": "Asessment created successfully",
                        "assessment": {
                            "id": 213,
                            "phq_score": 4,
                            "bdi_score": 3,
                            "plato_score": 30.7,
                            "protocol": "null",
                            "severity": 1,
                            "answers": [
                            {
                                "id": 367,
                                "assessment": 213,
                                "question": 5,
                                "answer": "answer 1",
                                "selected_option": {
                                    "id": 4,
                                    "label": "Option C - Q5",
                                    "value": "3"
                                },
                                "index": 0
                            },
                            {
                                "id": 368,
                                "assessment": 213,
                                "question": 9,
                                "answer": "answer 2",
                                "selected_option": {
                                    "id": 15,
                                    "label": "Option B - Q9",
                                    "value": "2"
                                },
                                "index": 3
                            },
                            {
                                "id": 369,
                                "assessment": 213,
                                "question": 10,
                                "answer": "answer 3",
                                "selected_option": {
                                    "id": 18,
                                    "label": "Option B - Q10",
                                    "value": "2"
                                },
                                "index": 3
                            }
                            ],
                            "suggested_protocols": [],
                            "created_at": "2025-07-21T15:26:28.457684Z"
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(description="BAD REQUEST"),
        401: OpenApiResponse(description="Authentication required"),
        403: OpenApiResponse(description="Must wait 4 weeks before creating a new assessment.")
    },
    tags=["Assessments"]
)

latest_assessment_schema = extend_schema(
    summary="Get latest assessment for profile",
    description="Retrieves the user's most recent assessment with suggested protocols and answers",
    tags=["Assessments"],
    responses={
        200: OpenApiResponse(
            description="Latest assessment with related data",
        ),
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(description="No assessment found"),
    },
)

