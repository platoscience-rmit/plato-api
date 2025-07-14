from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.assessments.serializers.assessment_serializer import AssessmentSerializer, SuggestedProtocolSerializer
from apps.assessments.services.assessment_service import AssessmentService
from apps.assessments.services.protocol_service import ProtocolService, SuggestedProtocolService


class AssessmentView(APIView):
    def post(self, request):
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                assessment = serializer.save()
                return Response(
                    {
                        'status': 'success',
                        'message': 'Asessment created successfully',
                        'assessment': assessment.id
                    }, 
                    status=status.HTTP_201_CREATED
                )
        
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
       
                
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
