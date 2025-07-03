from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.users.services.email_service import EmailService
from apps.users.services.user_service import UserService
from apps.users.serializers.user_serializer import UpdatePasswordSerializer
from apps.users.views.user_view import UpdateUserPasswordView
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

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {'error': 'Email is required'},
            )
        
        user = UserService().filter(email=email).first()
        if not user:
            return Response(
                {'error': 'User with this email does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        success, message = EmailService().send_forgot_password_email(user)
        if success:
            return Response(
                {'message': message},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': message},
            status=status.HTTP_400_BAD_REQUEST
        )
    
class VerifyForgotPasswordCodeView(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get('email')
            code = data.get('code')
            if not email or not code:
                return Response(
                    {'error': 'Email and code are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
           
            if EmailService().verify_forgot_password_code(email, code):
                return Response(
                    {'message': 'Code verified successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Invalid or expired code'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )