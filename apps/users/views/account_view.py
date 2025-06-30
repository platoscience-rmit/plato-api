from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.services.account_service import AccountService
from apps.users.serializers.account_serializer import AccountSerializer
from rest_framework.permissions import IsAuthenticated

class AccountListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = AccountService().get_all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            account_service = AccountService()
            account = account_service.authenticate_user(email, password)
            if not account:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
            tokens = account_service.generate_tokens(account.user_id)
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
    def __init__(self):
        super().__init__()
        self.account_service = AccountService()  
    
    def post(self, request):
        self.account_service.logout_user()  
        
        return Response(
            {
                'status': 'success',
                'message': 'Logout successful'
            },
            status=status.HTTP_200_OK
        )

class CreateAccountView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():
            account = serializer.save()
            return Response(
                {
                    'status': 'success',
                    'message': 'Account created successfully',
                    'user': {
                        'email': account.email,
                        'user_id': account.id
                    }
                }, 
                status=status.HTTP_201_CREATED
            )
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
