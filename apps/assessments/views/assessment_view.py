from apps.assessments.services.assessment_service import AssessmentService
from apps.assessments.serializers.assessment_serializer import AssessmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.assessments.schemas.assessment_schema import assessment_list_schema

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
