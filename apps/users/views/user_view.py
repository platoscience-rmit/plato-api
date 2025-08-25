from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.services.user_service import UserService
from rest_framework.permissions import IsAuthenticated
from apps.users.schemas.user_schemas import user_create_schema, login_schema, logout_schema, update_user_password_schema, me_schema
from apps.users.serializers.user_serializer import UserSerializer, UpdatePasswordSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes

@permission_classes([])
class UserView(APIView):
     
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        
        return [permission() for permission in permission_classes]

    def get(self, request):
        user = request.user
        if not user.is_staff:
            return Response(
                {'error': 'Only staff user can view all accounts'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        users = UserService().get_all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @user_create_schema
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if UserService().get_by_email(request.data.get('email')):
            existing_user = UserService().get_by_email(request.data.get('email'))
            if not existing_user.is_verified:
                return Response(
                    {'error': 'Email already exists but not verified'},
                    status=status.HTTP_409_CONFLICT
                )

        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data.copy()
                password = validated_data.pop('password')
                user = UserService().create(**validated_data)
                user.set_password(password)
                user.save()
                return Response(
                    {
                        'status': 'success',
                        'message': 'User created successfully',
                        'user': {
                            'email': serializer.validated_data['email'],
                            'user_id': user.id
                        }
                    }, 
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        return Response(
            {'error': 'Validation failed', 'details': serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@permission_classes([])
@authentication_classes([])
class LoginView(APIView):
    
    @login_schema
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = UserService().get_by_email(email)
            if not user or not user.check_password(password):
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
            if user.is_verified is False:
                return Response({"error": "Email not verified"}, status=status.HTTP_403_FORBIDDEN)
            
            tokens = UserService().generate_tokens(user)
            response = Response({"message": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=tokens['access'],
                httponly=True,
                secure=True,
                samesite='Lax',
            )
            response.set_cookie(
                key="refresh_token",
                value=tokens['refresh'],
                httponly=True,
                secure=True,
                samesite='Lax',
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    @logout_schema
    def post(self, request):
        try:
            response = Response(
                {
                    'status': 'success',
                    'message': 'Logout successful'
                },
                status=status.HTTP_200_OK
            )
            response.delete_cookie('access_token')
            return response
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
@permission_classes([])
class UpdateUserPasswordView(APIView):

    @update_user_password_schema
    def post(self, request):
        try:
            serializer = UpdatePasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'error': 'Invalid data', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            
            user = UserService().get_by_email(email)
            if not user:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            if not user.forgot_password_code_verified_at:
                return Response(
                    {'error': 'user forgot password code is not verified'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            user.set_password(new_password)
            user.forgot_password_code_verified_at = None
            user.forgot_password_code_expires = None
            user.save()
            return Response(
                {'message': 'Password updated successfully'},
                status=status.HTTP_200_OK
            )
                
        except Exception as e:
            return Response(
                {'error': f'Error updating password: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
@me_schema
class MeView(APIView):
    def get(self, request):
        user = request.user
        
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)