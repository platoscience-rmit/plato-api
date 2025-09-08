from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.assessments.serializers.assessment_serializer import (
    AssessmentSerializer,
    CreateAssessmentSerializer
)

from apps.common.serializer import (
    ErrorResponseSerializer,
)

assessment_list_schema = extend_schema(
    summary="List Assessments",
    description="Retrieve a list of assessments that selected a protocol and latest assessment for the authenticated user.",
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
        401: OpenApiResponse(
            description="Authentication required",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Error response",
                    value={
                        "detail": "Authentication credentials were not provided."
                    }
                )
            ]
        ),
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
                    },
                    {
                    "question": 11,
                    "answer": "I wake up tired, even after sleeping. Everything feels heavy — getting out of bed, brushing my teeth, replying to a message. I'm constantly drained, like my battery’s always at 10%. I go through the day pretending I’m okay, but inside I feel numb or low. Sometimes I cry for no reason, other times I feel nothing at all. I avoid people, but being alone makes me feel worse. There's guilt, like I'm failing at life, and a quiet voice that keeps asking, what’s the point?",
                    "selected_option": None,
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
                        "depression_type": "None",
                        "analysis": "The individual reports a constellation of symptoms including persistent low mood, fatigue, lack of motivation, difficulty concentrating, disrupted sleep, irregular eating habits, social withdrawal, feelings of guilt, recurring intrusive thoughts, hopelessness, emotional numbness, and unpredictable episodes of sadness or anxiety. These symptoms cause significant distress and make daily tasks feel overwhelmingly difficult and emotionally draining, although the individual is still able to function. The symptoms described do not clearly align with a specific duration, making it difficult to definitively diagnose Major Depressive Disorder (at least two weeks) or Persistent Depressive Disorder (at least two years in adults). Further questioning about the duration and specific triggers or causes is needed to differentiate between possible diagnoses.",
                        "assessment": {
                            "id": 252,
                            "phq_score": 4,
                            "bdi_score": 3,
                            "plato_score": 30.7,
                            "protocol": None,
                            "severity": 1,
                            "answers": [
                            {
                                "id": 486,
                                "assessment": 252,
                                "question": {
                                    "name": "bdi_q1",
                                    "content": "I do not feel sad / I feel sad / I am sad all the time",
                                    "description": "BDI Question 1",
                                    "category": "bdi",
                                    "options": [
                                        {
                                            "id": 2,
                                            "label": "Option A - Q5",
                                            "value": "1"
                                        },
                                        {
                                            "id": 3,
                                            "label": "Option B - Q5",
                                            "value": "2"
                                        },
                                        {
                                            "id": 4,
                                            "label": "Option C - Q5",
                                            "value": "3"
                                        }
                                    ],
                                    "type": "radio"
                                },
                                "answer": "answer 1",
                                "selected_option": {
                                    "id": 4,
                                    "label": "Option C - Q5",
                                    "value": "3"
                                },
                                "index": 0
                            },
                            {
                                "id": 487,
                                "assessment": 252,
                                "question": {
                                "name": "phq_q2",
                                "content": "Feeling down, depressed, or hopeless?",
                                "description": "PHQ Question 2",
                                "category": "phq",
                                "options": [
                                    {
                                        "id": 14,
                                        "label": "Option A - Q9",
                                        "value": "1"
                                    },
                                    {
                                        "id": 15,
                                        "label": "Option B - Q9",
                                        "value": "2"
                                    },
                                    {
                                        "id": 16,
                                        "label": "Option C - Q9",
                                        "value": "3"
                                    }
                                ],
                                "type": "radio"
                                },
                                "answer": "answer 2",
                                "selected_option": {
                                    "id": 15,
                                    "label": "Option B - Q9",
                                    "value": "2"
                                    },
                                "index": 3
                            },
                            {
                                "id": 488,
                                "assessment": 252,
                                "question": {
                                    "name": "phq_q3",
                                    "content": "Trouble falling or staying asleep?",
                                    "description": "PHQ Question 3",
                                    "category": "phq",
                                    "options": [
                                        {
                                            "id": 17,
                                            "label": "Option A - Q10",
                                            "value": "1"
                                        },
                                        {
                                            "id": 18,
                                            "label": "Option B - Q10",
                                            "value": "2"
                                        },
                                        {
                                            "id": 19,
                                            "label": "Option C - Q10",
                                            "value": "3"
                                        }
                                    ],
                                    "type": "checkbox"
                                },
                                "answer": "answer 3",
                                "selected_option": {
                                    "id": 18,
                                    "label": "Option B - Q10",
                                    "value": "2"
                                },
                                "index": 3
                            },
                            {
                                "id": 489,
                                "assessment": 252,
                                "question": {
                                    "name": "analytic 1",
                                    "content": "The individual experiences persistent low mood, fatigue, and a lack of motivation. They report difficulty concentrating, disrupted sleep patterns, and irregular eating habits. Although still able to function in daily life, tasks feel overwhelmingly difficult and emotionally draining. There is significant social withdrawal, feelings of guilt, and recurring intrusive thoughts that contribute to a sense of hopelessness. Emotional numbness alternates with unpredictable episodes of sadness or anxiety. Despite outwardly appearing functional, the internal distress is constant and exhausting.",
                                    "description": "The individual experiences persistent low mood, fatigue, and a lack of motivation. They report difficulty concentrating, disrupted sleep patterns, and irregular eating habits. Although still able to function in daily life, tasks feel overwhelmingly difficult and emotionally draining. There is significant social withdrawal, feelings of guilt, and recurring intrusive thoughts that contribute to a sense of hopelessness. Emotional numbness alternates with unpredictable episodes of sadness or anxiety. Despite outwardly appearing functional, the internal distress is constant and exhausting.",
                                    "category": "analytic",
                                    "options": [],
                                    "type": "text"
                                },
                                "answer": "The individual experiences persistent low mood, fatigue, and a lack of motivation. They report difficulty concentrating, disrupted sleep patterns, and irregular eating habits. Although still able to function in daily life, tasks feel overwhelmingly difficult and emotionally draining. There is significant social withdrawal, feelings of guilt, and recurring intrusive thoughts that contribute to a sense of hopelessness. Emotional numbness alternates with unpredictable episodes of sadness or anxiety. Despite outwardly appearing functional, the internal distress is constant and exhausting.",
                                "selected_option": None,
                                "index": 3
                            }
                            ],
                            "suggested_protocols": [
                                {
                                    "first_protocol": None,
                                    "second_protocol": None,
                                    "third_protocol": None
                                }
                            ],
                            "protocol_selected_date": None,
                            "stopped_date": None,
                            "stop_reason": None,
                            "created_at": "2025-08-01T11:15:43.240486Z"
                        }
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="BAD REQUEST",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Error response",
                    value={
                        "error": "Error creating assessment: Selected option (id=4) does not belong to question (id=4) or not active"
                    }
                )
            ]
        ),
        401: OpenApiResponse(
            description="Authentication required",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Error response",
                    value={
                        "detail": "Authentication credentials were not provided."
                    }
                )
            ]
        ),
        403: OpenApiResponse(description="Invalid input")
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
            response=AssessmentSerializer(),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "id": 79,
                        "phq_score": 3,
                        "bdi_score": 0,
                        "plato_score": 26.7,
                        "protocol": None,
                        "severity": 1,
                        "checkin_days_count": 0,
                        "answers": [
                            {
                                "id": 205,
                                "assessment": 79,
                                "question": {
                                    "id": 5,
                                    "name": "q6",
                                    "content": "Feeling tired or having little energy?",
                                    "description": "PHQ item 2",
                                    "category": "phq",
                                    "options": [
                                    {
                                        "id": 7,
                                        "label": "Not at all",
                                        "value": "0"
                                    },
                                    {
                                        "id": 8,
                                        "label": "Several days",
                                        "value": "1"
                                    },
                                    {
                                        "id": 9,
                                        "label": "More than half the days",
                                        "value": "2"
                                    },
                                    {
                                        "id": 10,
                                        "label": "Nearly every day",
                                        "value": "3"
                                    },
                                    {
                                        "id": 4,
                                        "label": "Nearly every day",
                                        "value": "3"
                                    }
                                    ],
                                    "type": "radio",
                                    "is_active": True
                                },
                                "answer": "answer 1",
                                "selected_option": {
                                    "id": 4,
                                    "label": "Nearly every day",
                                    "value": "3"
                                },
                                "index": 0
                            },
                            {
                                "id": 206,
                                "assessment": 79,
                                "question": {
                                    "id": 9,
                                    "name": "q10",
                                    "content": "Do you think your current protocol is effective?",
                                    "description": "Analytic feedback",
                                    "category": "analytic",
                                    "options": [
                                    {
                                        "id": 23,
                                        "label": "Not at all",
                                        "value": "0"
                                    },
                                    {
                                        "id": 24,
                                        "label": "Several days",
                                        "value": "1"
                                    },
                                    {
                                        "id": 25,
                                        "label": "More than half the days",
                                        "value": "2"
                                    },
                                    {
                                        "id": 26,
                                        "label": "Nearly every day",
                                        "value": "3"
                                    },
                                    {
                                        "id": 15,
                                        "label": "Not at all",
                                        "value": "0"
                                    }
                                    ],
                                    "type": "select",
                                    "is_active": True
                                },
                                "answer": "answer 2",
                                "selected_option": {
                                    "id": 15,
                                    "label": "Not at all",
                                    "value": "0"
                                },
                                "index": 3
                            },
                            {
                                "id": 207,
                                "assessment": 79,
                                "question": {
                                    "id": 10,
                                    "name": "q4",
                                    "content": "How do you feel right now?",
                                    "description": "Check-in question",
                                    "category": "check-in",
                                    "options": [
                                    {
                                        "id": 18,
                                        "label": "Always",
                                        "value": "3"
                                    }
                                    ],
                                    "type": "textarea",
                                    "is_active": True
                                },
                                "answer": "answer 3",
                                "selected_option": {
                                    "id": 18,
                                    "label": "Always",
                                    "value": "3"
                                },
                                "index": 3
                                },
                                {
                                "id": 208,
                                "assessment": 79,
                                "question": {
                                    "id": 11,
                                    "name": "q11",
                                    "content": "How do you feel right now?",
                                    "description": "Check-in question",
                                    "category": "check-in",
                                    "options": [],
                                    "type": "textarea",
                                    "is_active": True
                                },
                                "answer": "I wake up tired, even after sleeping. Everything feels heavy — getting out of bed, brushing my teeth, replying to a message. I'm constantly drained, like my battery’s always at 10%. I go through the day pretending I’m okay, but inside I feel numb or low. Sometimes I cry for no reason, other times I feel nothing at all. I avoid people, but being alone makes me feel worse. There's guilt, like I'm failing at life, and a quiet voice that keeps asking, what’s the point?",
                                "selected_option": None,
                                "index": 3
                            }
                        ],
                        "suggested_protocols": [
                            {
                            "first_protocol": {
                                "id": 25,
                                "intensity": "medium",
                                "duration": "11min",
                                "node_placement": "Node2",
                                "node_type": "cathode",
                                "node_size": "5x5",
                                "norm_study_id": "27",
                                "norm_study_code": "CODE27",
                                "tdcs_total_session": "12",
                                "tdcs_session_per_week": "3",
                                "tdcs_weeks": "5",
                                "reference": "H. Hausman et al., \"tDCS reduces depress…\""
                            },
                            "second_protocol": {
                                "id": 39,
                                "intensity": "low",
                                "duration": "10min",
                                "node_placement": "Node1",
                                "node_type": "anode",
                                "node_size": "5x7",
                                "norm_study_id": "21",
                                "norm_study_code": "CODE26",
                                "tdcs_total_session": "11",
                                "tdcs_session_per_week": "2",
                                "tdcs_weeks": "4",
                                "reference": "R. Woodham et al., \"Home-based transcranial…\""
                            },
                            "third_protocol": {
                                "id": 41,
                                "intensity": "high",
                                "duration": "12min",
                                "node_placement": "Node3",
                                "node_type": "anode",
                                "node_size": "5x7",
                                "norm_study_id": "23",
                                "norm_study_code": "CODE28",
                                "tdcs_total_session": "13",
                                "tdcs_session_per_week": "4",
                                "tdcs_weeks": "6",
                                "reference": "A. Dragon et al., \"Treating depression at…\""
                            }
                            }
                        ],
                        "protocol_selected_date": None,
                        "stopped_date": None,
                        "stop_reason": None,
                        "depression_type": "None",
                        "short_depression_type": "N",
                        "analysis": "The user provided an insufficient response ('answer 2') to determine a likely depression type. More information about the user's symptoms, duration, and potential causes is needed to provide an accurate analysis.",
                        "created_at": "2025-09-08T00:41:03.976227Z"
                    }
                )
            ]
        ),
        401: OpenApiResponse(
            description="Authentication required",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Error response",
                    value={
                        "detail": "Authentication credentials were not provided."
                    }
                )
            ]
        ),
        404: OpenApiResponse(description="No assessment found"),
    },
)

select_protocol_schema = extend_schema(
    summary="Select Protocol for latest assessment",
    description="Update the user's latest assessment with one of the suggested protocols.",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'protocolId': {
                    'type': 'integer',
                    'description': 'ID of the protocol'
                }
            },
            'required': ['protocolId']
        }
    },
    examples=[
        OpenApiExample(
            'Example Request',
            value={
                "protocolId": 2
            },
            request_only=True,
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Protocol selected successfully",
            response=AssessmentSerializer(),
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "id": 1,
                        "phq_score": 15,
                        "bdi_score": 30,
                        "plato_score": 3.5,
                        "protocol": {
                            "id": 2,
                            "intensity": "Medium",
                            "duration": "20 mins",
                            "node_placement": "Chest",
                            "node_type": "Type B",
                            "node_size": "Medium"
                        },
                        "severity": 2,
                        "answers": [],
                        "suggested_protocols": [
                            {
                                "id": 1,
                                "first_protocol": {
                                    "id": 1,
                                    "intensity": "High",
                                    "duration": "30 mins",
                                    "node_placement": "Head",
                                    "node_type": "Type A",
                                    "node_size": "Large"
                                },
                                "second_protocol": {
                                    "id": 2,
                                    "intensity": "Medium",
                                    "duration": "20 mins",
                                    "node_placement": "Chest",
                                    "node_type": "Type B",
                                    "node_size": "Medium"
                                },
                                "third_protocol": {
                                    "id": 3,
                                    "intensity": "Low",
                                    "duration": "15 mins",
                                    "node_placement": "Forehead",
                                    "node_type": "Type C",
                                    "node_size": "Small"
                                }
                            }
                        ],
                        "created_at": "2025-08-04T16:43:06.802369Z"
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request - protocolId is required or invalid protocol selection",
            examples=[
                OpenApiExample(
                    "Missing protocolId",
                    value={"error": "protocolId is required"}
                ),
                OpenApiExample(
                    "Invalid protocol selection",
                    value={
                        "error": "Invalid protocol selection. You can only choose from suggested protocols: [1, 2, 3]",
                        "valid_protocol_ids": [1, 2, 3]
                    }
                )
            ]
        ),
        404: OpenApiResponse(
            description="Not Found - No assessment or suggested protocols found",
            examples=[
                OpenApiExample(
                    "No assessment found",
                    value={"error": "No assessment found for user"}
                ),
                OpenApiExample(
                    "No suggested protocols",
                    value={"error": "No suggested protocols found for this assessment"}
                )
            ]
        ),
        401: OpenApiResponse(
            description="Authentication required",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Error response",
                    value={
                        "detail": "Authentication credentials were not provided."
                    }
                )
            ]
        ),
        500: OpenApiResponse(description="Internal server error")
    },
    tags=["Assessments"]
)

stop_assessment_schema = extend_schema(
    summary="Stop an assessment",
    description="Stop the latest assessment with a provided stop reason.",
    tags=["Assessments"],
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "Reason for stopping the assessment"
                }
            },
            "required": ["reason"]
        }
    },
    examples=[
        OpenApiExample(
            "Example Request",
            value={"reason": "User requested stop"},
            request_only=True
        ),
        OpenApiExample(
            "Success Response",
            value={
                "id": 1,
                "user": 5,
                "protocol_selected_date": "2025-04-13",
                "stopped_date": "2025-08-03T12:00:00Z",
                "stop_reason": "User requested stop",
            },
            response_only=True
        ),
        OpenApiExample(
            "Missing Reason",
            value={"error": "reason is not provided"},
            response_only=True
        )
    ],
    responses={
        200: OpenApiResponse(
            description="Stop assessment successfully",
        ),
        401: OpenApiResponse(
            description="Authentication required",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Error response",
                    value={
                        "detail": "Authentication credentials were not provided."
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Bad Request",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Error response",
                    value={
                        "error": "This assessment is not active"
                    }
                )
            ]
        ),
        404: OpenApiResponse(description="No assessment found"),
    }
)

can_assess_schema = extend_schema(
    summary="Check current reassessment status",
    description="Check if user is allowed to reassess and if not, return the remain time.",
    tags=["Assessments"],
    responses={
        200: OpenApiResponse(
            description="Return reassessment state successfully",
            response={
                "type": "object",
                "properties": {
                    "isAllowed": {"type": "boolean"},
                    "remainTime": {"type": "int"},
                    "error": {"type": "string"},
                    "remainAssess": {"type": "int"},
                }
            },
            examples=[
                OpenApiExample(
                    'Allow Response',
                    value={
                        "isAllowed": True,
                        "remainTime": None,
                        "remainAssess": 4 
                    },
                    response_only=True,
                    status_codes=['200']
                ),
                OpenApiExample(
                    'Blocked Response',
                    value={
                        "isAllowed": False,
                        "remainTime": 3600,
                        "remainAssess": 0  
                    },
                    response_only=True,
                    status_codes=['200']
                )
            ]
        ),
        401: OpenApiResponse(
            description="Authentication required",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Error response",
                    value={
                        "detail": "Authentication credentials were not provided."
                    }
                )
            ]
        ),
        403: OpenApiResponse(
            description="Forbiden due to active assessment",
            response={
                "type": "object",
                "properties": {
                    "isAllowed": {"type": "boolean"},
                    "remainTime": {"type": "int"},
                    "error": {"type": "string"}
                }
            },
            examples=[
                OpenApiExample(
                    'Example Response',
                    value={
                        'isAllowed': False,
                        'remainTime': None,
                        'error': 'You cannot create a new assessment with an active assessment.'
                    },
                    response_only=True,
                    status_codes=['403']
                )
            ]
        ),
    }
)
stop_assessment_period_schema = extend_schema(
    summary="Stop expired assessment",
    description="Stops assessments that have expired (over 4 weeks with a protocol or 2 weeks without one), sends a notification to the user, and marks them as ended",
    tags=["Assessments"],
    responses={
        200: OpenApiResponse(
            description="Success Reponse",
            response={
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "message": {"type": "string"}
                }
            },
            examples=[
                OpenApiExample(
                    'Success Response',
                    value={
                        'status': 'success',
                        'message': "Stopped 0 assessments.",
                    }
                )
            ]
        ),
        401: OpenApiResponse(
            description="Authentication required",
            response=ErrorResponseSerializer,
            examples=[
                OpenApiExample(
                    "Error response",
                    value={
                        "detail": "Authentication credentials were not provided."
                    }
                )
            ]
        )
    }
)