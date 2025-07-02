from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.users.services.email_service import EmailService
from apps.users.services.user_service import UserService

class VerifyEmailView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response(
                {'error': 'Token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success, message = EmailService().verify_email(token)
        if success:
            return Response(
                {'message': message},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class ResendVerificationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'error': 'User is not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if user.is_verified:
            return Response(
                {'message': 'User is already verified'},
                status=status.HTTP_200_OK
            )
        
        success, message = EmailService().resend_verification_email(user)
        if success:
            return Response(
                {'message': message},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': message},
            status=status.HTTP_400_BAD_REQUEST
        )
