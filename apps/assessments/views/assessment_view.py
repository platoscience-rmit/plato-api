from apps.assessments.services.assessment_service import AssessmentService
from apps.assessments.serializers.assessment_serializer import AssessmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.assessments.schemas.assessment_schema import assessment_list_schema, latest_assessment_schema
from apps.assessments.models import Assessment

class AssessmentView(APIView):
    def __init__(self):
        self.service = AssessmentService()

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

class LatestAssessmentView(APIView):
    permission_classes = [IsAuthenticated]

    @latest_assessment_schema
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        latest_assessment = (
            Assessment.objects
            .filter(user=user)
            .select_related('protocol')
            .prefetch_related('suggested_protocols', 'answers', 'answers__question')
            .order_by('-created_at')
            .first()
        )
        
        if not latest_assessment:
            return Response({'error': 'No assessment found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AssessmentSerializer(latest_assessment)
        data = serializer.data
        
        data['suggested_protocols'] = [
            {
                'id': sp.id,
                'first_protocol': {
                    'id': sp.first_protocol.id,
                    'intensity': sp.first_protocol.intensity,
                    'duration': sp.first_protocol.duration,
                    'node_placement': sp.first_protocol.node_placement,
                    'node_type': sp.first_protocol.node_type,
                    'node_size': sp.first_protocol.node_size,
                } if sp.first_protocol else None,
                'second_protocol': {
                    'id': sp.second_protocol.id,
                    'intensity': sp.second_protocol.intensity,
                    'duration': sp.second_protocol.duration,
                    'node_placement': sp.second_protocol.node_placement,
                    'node_type': sp.second_protocol.node_type,
                    'node_size': sp.second_protocol.node_size,
                } if sp.second_protocol else None,
                'third_protocol': {
                    'id': sp.third_protocol.id,
                    'intensity': sp.third_protocol.intensity,
                    'duration': sp.third_protocol.duration,
                    'node_placement': sp.third_protocol.node_placement,
                    'node_type': sp.third_protocol.node_type,
                    'node_size': sp.third_protocol.node_size,
                } if sp.third_protocol else None,
            }
            for sp in latest_assessment.suggested_protocols.all()
        ]
        
        return Response(data, status=status.HTTP_200_OK)