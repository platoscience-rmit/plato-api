from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.services.account_service import AccountService
from apps.users.serializers.account_serializer import AccountSerializer

class AccountListView(APIView):
    def get(self, request):
        accounts = AccountService().get_all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoginView(APIView):
    def __init__(self):
        super().__init__()
        self.account_service = AccountService() 
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        account = self.account_service.authenticate_user(username, password)  
        
        if account:
            return Response(
                {
                    'status': 'success',
                    'message': 'Login successful',
                    'user': {
                        'id': account.user_id.id,
                        'username': account.user_id.username,
                        'email': account.email,
                        'is_verified': account.is_verified
                    }
                }, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'status': 'error',
                    'message': 'Invalid username or password'
                }, 
                status=status.HTTP_401_UNAUTHORIZED
            )

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