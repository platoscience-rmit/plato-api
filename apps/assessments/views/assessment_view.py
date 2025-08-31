from django.utils import timezone
from apps.assessments.serializers.assessment_answer_serializer import AssessmentAnswerSerializer
from apps.assessments.services.assessment_service import AssessmentService
from apps.assessments.services.protocol_service import ProtocolService
from apps.assessments.serializers.assessment_serializer import AssessmentSerializer, CreateAssessmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.assessments.schemas.assessment_schema import assessment_list_schema, latest_assessment_schema, create_assessment_schema, select_protocol_schema, stop_assessment_schema, can_assess_schema
from apps.common.throttle import LimitAssessThrottle
from rest_framework.decorators import authentication_classes, permission_classes

class AssessmentView(APIView):
    def get_throttles(self):
        if self.request.method == "POST":
            return [LimitAssessThrottle()]
        return []
    
    def __init__(self):
        self.service = AssessmentService()

    def get_permissions(self):
        if self.request.method == "POST" or "PUT" or "DELETE":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    @assessment_list_schema
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        assessments = self.service.get_all_by_user(user)
        serializer = AssessmentSerializer(assessments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @create_assessment_schema
    def post(self, request):
        check = self.service.can_assess(request.user)
        if not check:
            return Response(
                {
                    'error': 'You cannot create a new assessment with an active assessment.'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        assessment_serializer = CreateAssessmentSerializer(data=request.data)

        if assessment_serializer.is_valid():
            try:
                assessment = AssessmentService().create_with_answer(
                    assessment_data=assessment_serializer.validated_data,
                    user=request.user
                )

                return Response(
                    {
                        'status': 'success',
                        'message': 'Asessment created successfully',
                        "depression_type": assessment["depression_type"],
                        "analysis": assessment["analysis"],
                        'assessment': AssessmentSerializer(assessment["assessment"]).data,
                    }, 
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    "errors": {
                        "assessment": assessment_serializer.errors,
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        

class CheckTimeIntervalView(APIView):
    def __init__(self):
        self.service = AssessmentService()

    def get_permissions(self):
        if self.request.method == "POST" or "PUT" or "DELETE":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def post(self, request):
        check = self.service.is_valid_time(request.user)
        return Response(
            {
                "is_valid": check['is_valid'],
                "next_valid_time": check['next_valid_time']
            },
            status=status.HTTP_200_OK if check['is_valid'] else status.HTTP_403_FORBIDDEN
        )

class LatestAssessmentView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.service = AssessmentService()

    @latest_assessment_schema
    def get(self, request):
        try:
            user = request.user
            latest_assessment = self.service.get_latest_by_user(user)

            if not latest_assessment:
                return Response({'error': 'No assessment found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = AssessmentSerializer(latest_assessment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SelectProtocolView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.assessment_service = AssessmentService()
        self.protocol_service = ProtocolService()

    @select_protocol_schema
    def post(self, request):
        try:
            protocol_id = request.data.get('protocolId')

            if not protocol_id:
                return Response(
                    {'error': 'protocolId is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            protocol = self.protocol_service.filter(id=protocol_id).first()
            if not protocol:
                return Response(
                    {'error': f'Protocol with id {protocol_id} not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            latest_assessment = self.assessment_service.get_latest_by_user(request.user)
            if not latest_assessment:
                return Response(
                    {'error': 'No assessment found for user'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            is_stopped = AssessmentService().get_latest_by_user(request.user).stopped_date is None
            
            if is_stopped:
                return Response(
                    {
                        'isAllowed': False,
                        'remainTime': None,
                        'error': 'You cannot select protocol for a stopped assessment.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            if not is_stopped and latest_assessment.protocol is not None:
                return Response(
                    {
                        'isAllowed': False,
                        'error': 'Protocol already selected for this active assessment.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            updated_assessment = self.assessment_service.update(
                latest_assessment.id, 
                protocol=protocol,
                protocol_selected_date=timezone.now()
            )

            serializer = AssessmentSerializer(updated_assessment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        

class AssessmentStopView(APIView):
    
    def __init__(self):
        self.service = AssessmentService()
        
    @stop_assessment_schema
    def post(self, request):
        try:
            user = request.user

            if self.service.is_stopped(user):
                return Response(
                    {'error': 'This assessment is not active already'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            reason = request.data.get('reason')
            if reason is None:
                return Response(          
                    {'error': 'reason is not provided'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            res = self.service.end_assessment(user, reason)
            serializer = AssessmentSerializer(res)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(          
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class CanAssessView(APIView):
    @can_assess_schema
    def get(self, request):
        try:
            can_assess = AssessmentService().can_assess(request.user)
            if not can_assess:
                return Response(
                    {
                        'isAllowed': False,
                        'remainTime': None,
                        'error': 'You cannot create a new assessment with an active assessment.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            is_allowed, wait, remain_assess = LimitAssessThrottle().get_current_state(request, self)
            return Response(
                {
                    'isAllowed': is_allowed,
                    'remainTime': wait,
                    'remainAssess': remain_assess
                }
            )
        except Exception as e:
            return Response(          
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
@permission_classes([])
@authentication_classes([]) 
class StopAssessmentPeriod(APIView):
    def __init__(self):
        self.service = AssessmentService()
        
    def get(self, request):
        try:
            updated_count = self.service.end_assessment_period()
            return Response(
                {"status": "success", "message": f"Stopped {updated_count} assessments."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )