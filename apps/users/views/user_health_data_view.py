from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers.user_health_data_serializer import UserHealthDataSerializer, UserHealthDataResponseSerializer
from apps.users.serializers.user_serializer import UserSerializer
from apps.users.services.user_health_data_service import UserHealthDataService
from rest_framework.permissions import IsAuthenticated
from apps.users.schemas.user_health_data_schemas import upload_health_data_schema, update_consent_health_data_schema
from apps.users.services.user_service import UserService

class UserHealthDataView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.service = UserHealthDataService()

    @upload_health_data_schema
    def post(self, request):
        serializer = UserHealthDataSerializer(data=request.data)
        try:
            serializer = UserHealthDataSerializer(data=request.data, context={'request': request})
            if not request.user.is_consent_health_data:
                return Response(
                    {
                        'message': 'Consent required'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            if serializer.is_valid():
                health_data = serializer.save()

                response_serializer = UserHealthDataResponseSerializer(health_data)

                return Response(
                    {
                        'message': 'Health data uploaded successfully',
                        'data': response_serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        'error': 'Invalid data',
                        'details': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateConsentHealthDataView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.service = UserHealthDataService()
    
    @update_consent_health_data_schema
    def post(self, request):
        try:
            user = request.user
            is_consent_health_data = request.data.get("is_consent_health_data", "__missing__")
            if is_consent_health_data == "__missing__":
                return Response(
                    {"detail": "Missing is_consent_health_data"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = UserService().update(
                pk=user.id, 
                is_consent_health_data=is_consent_health_data
            )
            
            return Response(
                    {
                        'message': 'Update consent successfully',
                        'data': UserSerializer(user).data
                    },
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
