from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.services.user_service import UserService
from apps.users.serializers.user_serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.schemas.user_schemas import user_create_schema
class UserView(APIView):
     
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        
        return [permission() for permission in permission_classes]

    def get(self, request):
        users = UserService().get_all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @user_create_schema
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = UserService().create(**serializer.validated_data)
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

class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = UserService().authenticate_user(email, password)
            if not user:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
            tokens = UserService().generate_tokens(user)
            response = Response({"message": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=tokens['access'],
                httponly=True,
                secure=True,
                samesite='Lax',
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
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
        